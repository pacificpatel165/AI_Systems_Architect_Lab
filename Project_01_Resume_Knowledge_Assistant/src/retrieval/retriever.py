import numpy as np
from src.logger import get_logger

logger = get_logger(__name__)


# ==========================================================
# Stop Words
# ==========================================================
STOP_WORDS = {
    "what",
    "which",
    "where",
    "when",
    "how",
    "have",
    "has",
    "had",
    "did",
    "does",
    "do",
    "used",
    "work",
    "worked",
    "i",
    "my",
    "the",
    "a",
    "an",
    "on",
    "in",
    "for",
}


# ==========================================================
# Keyword Search
# ==========================================================
def keyword_search(query, chunks):
    query_words = [word for word in query.lower().split() if word not in STOP_WORDS]
    results = []

    for idx, chunk in enumerate(chunks):
        chunk_text = chunk["text"].lower()
        score = 0
        for word in query_words:
            if word in chunk_text:
                score += 1

        if score > 0:
            results.append((idx, score))

    results.sort(key=lambda x: x[1], reverse=True)
    logger.debug("Keyword search returned %d matches", len(results))
    return [idx for idx, score in results]


# ==========================================================
# Semantic Search
# ==========================================================
def semantic_search(query, embedding_model, index, top_k=5):
    query_embedding = embedding_model.encode([query])
    distances, indices = index.search(
        np.array(query_embedding).astype("float32"), top_k
    )
    logger.info("Semantic search returned %d chunks", len(indices[0]))
    return indices[0].tolist()


# ==========================================================
# Hybrid Search
# ==========================================================
def hybrid_search(query, embedding_model, index, chunks, semantic_k=5, final_k=8):
    semantic_results = semantic_search(query, embedding_model, index, semantic_k)
    keyword_results = keyword_search(query, chunks)
    combined = []

    for idx in semantic_results:
        if idx not in combined:
            combined.append(idx)

    for idx in keyword_results:
        if idx not in combined:
            combined.append(idx)

    logger.info("Hybrid retrieval selected %d chunks", len(combined[:final_k]))
    return combined[:final_k]


# ==========================================================
# Inspect Retrieval
# ==========================================================
def inspect_retrieval(question, embedding_model, index, chunks):
    results = hybrid_search(
        question, embedding_model, index, chunks, semantic_k=10, final_k=10
    )

    print("\n" + "=" * 80)
    print(f"QUESTION: " f"{question}")
    print("=" * 80)
    for rank, idx in enumerate(results, start=1):
        chunk = chunks[idx]
        print()
        print(f"Rank={rank}")
        print(f"Chunk={idx}")
        print(f"Source={chunk['source_file']}")
        print(f"Page={chunk['page_number']}")
        print(chunk["text"][:300])
