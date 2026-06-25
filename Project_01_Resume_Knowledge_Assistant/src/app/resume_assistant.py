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
        index,
        chunks,
        parent_documents,
        conversation_memory,
    ):

        self.embedding_model = embedding_model
        self.reranker = reranker

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
            context = build_parent_context(parent_ids, self.parent_documents)
        else:
            parent_ids = []
            context = ""
            for idx in top_indices:
                context += self.chunks[idx]["text"] + "\n\n"

        # ------------------------------------------
        # Context Compression
        # ------------------------------------------
        if strategy["compression"]:
            context = compress_context(question, context, self.embedding_model)

        # ------------------------------------------
        # Return Everything
        # ------------------------------------------
        return {
            "query_type": query_type,
            "strategy": strategy,
            "rewritten_query": rewritten_query,
            "retrieved_indices": retrieved_indices,
            "ranked_results": ranked_results,
            "top_indices": top_indices,
            "parent_ids": parent_ids,
            "context": context,
            "document_filter": document_filter,
        }


    # ==========================================================
    # Debug Retrieval Result
    # ==========================================================
    def debug(self, result):
        print()
        print("=" * 100)
        print("RESUME ASSISTANT - RETRIEVAL RESULT")
        print("=" * 100)

        print("\nQUESTION TYPE")
        print("-" * 80)
        print(result["query_type"])

        print("\nRETRIEVAL STRATEGY")
        print("-" * 80)
        for key, value in result["strategy"].items():
            print(f"{key:<20}: {value}")

        print("\nREWRITTEN QUERY")
        print("-" * 80)
        print(result["rewritten_query"])

        print("\nDOCUMENT FILTER")
        print("-" * 80)
        print(result["document_filter"])

        print("\nRETRIEVED CHUNKS")
        print("-" * 80)
        print(result["retrieved_indices"])

        print("\nTOP CHUNKS")
        print("-" * 80)
        print(result["top_indices"])

        print("\nPARENT IDS")
        print("-" * 80)
        print(result["parent_ids"])

        print("\nCONTEXT")
        print("-" * 80)
        print(result["context"][:1000])

        print("=" * 100)
