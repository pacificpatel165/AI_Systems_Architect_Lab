import numpy as np
from src.config import ENABLE_KEYWORD_COMPRESSION, ENABLE_SEMANTIC_COMPRESSION
from src.logger import get_logger

logger = get_logger(__name__)


# ==========================================================
# Keyword Context Compression
# ==========================================================
def keyword_compress_context(question, context):
    query_words = {word.lower() for word in question.split() if len(word) > 2}
    lines = context.split("\n")
    compressed = []
    for line in lines:
        lower = line.lower()
        if any(word in lower for word in query_words):
            compressed.append(line)
    return "\n".join(compressed)


# ==========================================================
# Semantic Compression
# ==========================================================
def semantic_compress_context(question, context, embedding_model, top_n=20):
    lines = [line.strip() for line in context.split("\n") if len(line.strip()) > 20]
    if len(lines) == 0:
        return context
    query_embedding = embedding_model.encode([question])
    line_embeddings = embedding_model.encode(lines)
    similarities = np.dot(line_embeddings, query_embedding[0])
    ranked = np.argsort(similarities)[::-1]
    selected = []
    for idx in ranked[:top_n]:
        selected.append(lines[idx])
    return "\n".join(selected)


# ==========================================================
# Context Compression
# ==========================================================
def compress_context(question, context, embedding_model):
    compressed_context = context
    logger.debug("Starting context compression")
    if ENABLE_KEYWORD_COMPRESSION:
        compressed_context = keyword_compress_context(question, compressed_context)
        logger.debug(
            "Keyword compression reduced context from %d to %d characters",
            len(context),
            len(compressed_context),
        )
    if ENABLE_SEMANTIC_COMPRESSION:
        compressed_context = semantic_compress_context(
            question, compressed_context, embedding_model
        )
        logger.info("Context compressed to %d characters", len(compressed_context))
    return compressed_context


# ==========================================================
# Compression Statistics
# ==========================================================
def print_compression_stats(original, compressed):
    original_size = len(original)
    compressed_size = len(compressed)
    reduction = 100 * (1 - compressed_size / max(original_size, 1))
    print()
    print("=" * 80)
    print("CONTEXT COMPRESSION")
    print("=" * 80)
    print(f"Original Size : " f"{original_size}")
    print(f"Compressed Size : " f"{compressed_size}")
    print(f"Reduction : " f"{reduction:.2f}%")
