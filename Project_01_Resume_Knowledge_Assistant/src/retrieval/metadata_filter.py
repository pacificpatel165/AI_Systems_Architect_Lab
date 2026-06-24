# ==========================================================
# Metadata Filter
# ==========================================================
def get_document_filter(question):
    question = question.lower()

    # --------------------------------------
    # Certifications
    # --------------------------------------
    if any(
        word in question for word in ["certificate", "certification", "certifications"]
    ):
        return "certificate"

    # --------------------------------------
    # Projects
    # --------------------------------------
    words = question.split()
    if "project" in words or "projects" in words:
        return "project"

    # --------------------------------------
    # Notes
    # --------------------------------------
    if any(word in question for word in ["note", "notes", "study"]):
        return "notes"

    # --------------------------------------
    # Resume
    # --------------------------------------
    if "resume" in question:
        return "resume"

    # --------------------------------------
    # No Filter
    # --------------------------------------
    return None


# ==========================================================
# Filter Results
# ==========================================================
def filter_retrieved_results(retrieved_indices, chunks, document_type):
    # --------------------------------------
    # No Filter Required
    # --------------------------------------
    if document_type is None:
        return retrieved_indices

    filtered = []
    for idx in retrieved_indices:
        if chunks[idx]["document_type"] == document_type:
            filtered.append(idx)

    return filtered


# ==========================================================
# Metadata Debug
# ==========================================================
def print_metadata_filter(question, document_type):
    print()
    print("=" * 80)
    print("METADATA FILTER")
    print("=" * 80)

    print(f"Question      : {question}")
    print(f"Document Type : {document_type}")
