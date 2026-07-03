from src.logger import get_logger

logger = get_logger(__name__)


# ==========================================================
# Parent IDs
# ==========================================================
def get_parent_ids(top_indices, chunks):
    parent_ids = []
    for idx in top_indices:
        parent_id = chunks[idx]["parent_id"]
        if parent_id not in parent_ids:
            parent_ids.append(parent_id)
    logger.info("Retrieved %d unique parent documents", len(parent_ids))
    return parent_ids


# ==========================================================
# Parent Context
# ==========================================================
def build_parent_context(parent_ids, parent_documents):
    context = ""
    for parent_id in parent_ids:
        parent = parent_documents[parent_id]
        context += f"""
            Source File: {parent['source_file']}
            Document Type: {parent['document_type']}
            Page Number: {parent['page_number']}
            Content: {parent['text']}
            {'='*80}
        """
    logger.debug("Building context from %d parent documents", len(parent_ids))
    return context


# ==========================================================
# Parent Statistics
# ==========================================================
def print_parent_summary(parent_ids, parent_documents):
    print()
    print("=" * 80)
    print("PARENT RETRIEVAL")
    print("=" * 80)
    print(f"Parents Retrieved : " f"{len(parent_ids)}")
    print()
    for parent_id in parent_ids:
        parent = parent_documents[parent_id]
        print(
            f"Parent {parent_id}"
            f" | "
            f"{parent['source_file']}"
            f" | "
            f"Page "
            f"{parent['page_number']}"
        )
