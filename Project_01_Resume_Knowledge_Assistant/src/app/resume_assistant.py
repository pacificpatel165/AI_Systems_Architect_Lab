from src.llm.gemini_client import (
    generate_response,
)
from src.config import *
from src.rewriting.query_rewriter import rewrite_query
from src.retrieval.strategy import (
    classify_question,
    get_retrieval_strategy,
)
from src.retrieval.retriever import hybrid_search
from src.retrieval.metadata_filter import (
    get_document_filter,
    filter_retrieved_results,
)
from src.retrieval.reranker import (
    rerank_results,
    get_top_reranked,
)
from src.retrieval.parent_retriever import (
    get_parent_ids,
    build_parent_context,
)
from src.retrieval.compressor import compress_context
from src.memory.conversation_memory import build_memory_context, save_to_memory
from src.prompts.prompts import PROMPT_TEMPLATE
import time


# ==========================================================
# Resume Assistant
# ==========================================================
class ResumeAssistant:
    # ======================================================
    # Constructor
    # ======================================================
    def __init__(
        self,
        embedding_model,
        reranker,
        llm_model,
        index,
        chunks,
        parent_documents,
        conversation_memory,
    ):

        self.embedding_model = embedding_model
        self.reranker = reranker
        self.llm_model = llm_model

        self.index = index
        self.chunks = chunks
        self.parent_documents = parent_documents

        self.conversation_memory = conversation_memory

    # ======================================================
    # Retrieval Pipeline
    # ======================================================
    def _retrieve(self, question):
        # ------------------------------------------
        # Query Classification
        # ------------------------------------------
        query_type = classify_question(question)
        strategy = get_retrieval_strategy(query_type)

        # ------------------------------------------
        # Query Rewrite
        # ------------------------------------------
        if strategy["rewrite"]:
            rewritten_query = rewrite_query(question, self.conversation_memory)
        else:
            rewritten_query = question

        # ------------------------------------------
        # Hybrid Search
        # ------------------------------------------
        retrieved_indices = hybrid_search(
            rewritten_query,
            self.embedding_model,
            self.index,
            self.chunks,
            semantic_k=10,
            final_k=10,
        )

        # ------------------------------------------
        # Metadata Filter
        # ------------------------------------------
        if strategy["metadata"]:
            document_filter = get_document_filter(question)
            retrieved_indices = filter_retrieved_results(
                retrieved_indices, self.chunks, document_filter
            )
        else:
            document_filter = None

        # ------------------------------------------
        # Reranking
        # ------------------------------------------
        ranked_results = rerank_results(
            rewritten_query, retrieved_indices, self.chunks, self.reranker
        )
        top_indices = get_top_reranked(ranked_results, top_n=3)

        # ------------------------------------------
        # Parent Retrieval
        # ------------------------------------------
        if strategy["parent"]:
            parent_ids = get_parent_ids(top_indices, self.chunks)
            original_context = build_parent_context(parent_ids, self.parent_documents)
        else:
            parent_ids = []
            original_context = ""
            for idx in top_indices:
                original_context += self.chunks[idx]["text"] + "\n\n"

        # ------------------------------------------
        # Context Compression
        # ------------------------------------------
        compressed_context = original_context
        if strategy["compression"]:
            compressed_context = compress_context(
                question, original_context, self.embedding_model
            )

        # ------------------------------------------
        # Retrieve Sources for Citation
        # ------------------------------------------
        sources = []
        for idx in top_indices:
            chunk = self.chunks[idx]
            sources.append(
                {
                    "source_file": chunk["source_file"],
                    "page": chunk["page_number"],
                    "document_type": chunk["document_type"],
                }
            )
        # ------------------------------------------
        # Return Everything
        # ------------------------------------------
        retrieval_result = {
            # ---------------------------------------
            # Query
            # ---------------------------------------
            "question": question,
            "rewritten_query": rewritten_query,
            "query_type": query_type,
            "strategy": strategy,
            # ---------------------------------------
            # Metadata
            # ---------------------------------------
            "document_filter": document_filter,
            # ---------------------------------------
            # Retrieval
            # ---------------------------------------
            "retrieved_indices": retrieved_indices,
            "ranked_results": ranked_results,
            "top_indices": top_indices,
            "parent_ids": parent_ids,
            "sources": sources,
            # ---------------------------------------
            # Context
            # ---------------------------------------
            "original_context": original_context,
            "compressed_context": compressed_context,
            # ---------------------------------------
            # Statistics
            # ---------------------------------------
            "original_length": len(original_context),
            "compressed_length": len(compressed_context),
            "compression_ratio": (
                100 * (1 - len(compressed_context) / max(len(original_context), 1))
            ),
            # ---------------------------------------
            # Memory
            # ---------------------------------------
            "memory_size": len(self.conversation_memory),
        }
        return retrieval_result

    # ==========================================================
    # Build Prompt
    # ==========================================================
    def _build_prompt(self, question, retrieval_result):
        memory_context = build_memory_context(
            self.conversation_memory, MAX_MEMORY_TURNS
        )
        prompt = PROMPT_TEMPLATE.format(
            memory=memory_context,
            context=retrieval_result["compressed_context"],
            question=question,
        )
        return prompt

    # ==========================================================
    # Generate Answer
    # ==========================================================
    def _generate_answer(self, prompt):
        if not USE_LLM:
            return "LLM Disabled."
        try:
            answer = generate_response(self.llm_model, prompt)
        except Exception as e:
            answer = f"LLM Error: {e}"
        return answer

    # ==========================================================
    # Update Memory
    # ==========================================================
    def _update_memory(self, question, answer, retrieval_result):
        save_to_memory(
            question=question,
            answer=answer,
            top_indices=retrieval_result["top_indices"],
            chunks=self.chunks,
            conversation_memory=self.conversation_memory,
        )

    # ==========================================================
    # Debug Dashboard
    # ==========================================================
    def _debug(self, retrieval_result, answer):
        print()
        print("=" * 100)
        print("                                   RESUME ASSISTANT DEBUG")
        print("=" * 100)

        print("\n✓ QUESTION")
        print("-" * 80)
        print(retrieval_result["question"])

        print("\n✓ QUERY TYPE")
        print("-" * 80)
        print(retrieval_result["query_type"])

        print("\n✓ RETRIEVAL STRATEGY")
        print("-" * 80)
        print(retrieval_result["strategy"])

        print("\n✓ REWRITTEN QUERY")
        print("-" * 80)
        print(retrieval_result["rewritten_query"])

        print("\n✓ DOCUMENT FILTER")
        print("-" * 80)
        print(retrieval_result["document_filter"])

        print("\n✓ HYBRID SEARCH")
        print("-" * 80)
        print(f"Retrieved Chunks : " f"{len(retrieval_result['retrieved_indices'])}")

        print("\n✓ RERANKER")
        print("-" * 80)
        for rank, (idx, score) in enumerate(
            retrieval_result["ranked_results"], start=1
        ):
            print(f"Rank {rank:<2}" f"Chunk {idx:<4}" f"Score {score:.4f}")

        print("\n✓ PARENT DOCUMENTS")
        print("-" * 80)
        print(retrieval_result["parent_ids"])

        print("\n✓ CONTEXT COMPRESSION")
        print("-" * 80)
        print(f"Original Length    : " f"{retrieval_result['original_length']}")
        print(f"Compressed Length  : " f"{retrieval_result['compressed_length']}")
        print(f"Compression Ratio  : " f"{retrieval_result['compression_ratio']:.2f}%")

        print("\n✓ CONTEXT PREVIEW")
        print("-" * 80)
        print(retrieval_result["compressed_context"][:1000])

        print("\n✓ CONVERSATION MEMORY")
        print("-" * 80)
        print(f"Conversation Turns : " f"{retrieval_result['memory_size']}")

        print("\n✓ FINAL ANSWER")
        print("-" * 80)
        print(answer)
        print("=" * 100)

    # ==========================================================
    # Ask Assistant
    # ==========================================================
    def ask(self, question):
        start_time = time.perf_counter()
        # --------------------------------------
        # Retrieval
        # --------------------------------------
        retrieval_result = self._retrieve(question)

        # --------------------------------------
        # Prompt
        # --------------------------------------
        prompt = self._build_prompt(question, retrieval_result)

        # --------------------------------------
        # LLM
        # --------------------------------------
        answer = self._generate_answer(prompt)

        # --------------------------------------
        # Memory
        # --------------------------------------
        if DEBUG_MODE:
            self._debug(retrieval_result, answer)
        self._update_memory(question, answer, retrieval_result)
        latency = time.perf_counter() - start_time
        return {
            "question": question,
            "answer": answer,
            "sources": retrieval_result["sources"],
            "debug": retrieval_result,
            "latency": latency,
            "success": True,
        }
