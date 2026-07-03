from sentence_transformers import CrossEncoder
from src.logger import get_logger

logger = get_logger(__name__)


def load_reranker_model(model_name):
    reranker = CrossEncoder(model_name)
    logger.info(f"Loaded {model_name}")
    return reranker


# ==========================================================
# Rerank Results
# ==========================================================
def rerank_results(query, retrieved_indices, chunks, reranker):
    pairs = []
    logger.debug("Reranking %d retrieved chunks", len(retrieved_indices))
    for idx in retrieved_indices:
        pairs.append([query, chunks[idx]["text"]])

    scores = reranker.predict(pairs)
    ranked_results = sorted(
        zip(retrieved_indices, scores), key=lambda x: x[1], reverse=True
    )
    logger.info("Top reranked results: %d", len(ranked_results))
    return ranked_results


# ==========================================================
# Top Ranked Results
# ==========================================================
def get_top_reranked(ranked_results, top_n=3):
    return [idx for idx, score in ranked_results[:top_n]]


# ==========================================================
# Debug Reranker
# ==========================================================
def print_reranked_results(ranked_results):
    print()
    print("=" * 80)
    print("RERANKED RESULTS")
    print("=" * 80)

    for rank, (idx, score) in enumerate(ranked_results, start=1):
        logger.info("Rank=%d  Chunk=%d  Score=%.4f", rank, idx, score)
