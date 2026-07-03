from pypdf import PdfReader
import os
from src.logger import get_logger

logger = get_logger(__name__)


# ==========================================================
# Document Type
# ==========================================================
def infer_document_type(source_file):
    filename = source_file.lower()
    if "certificate" in filename:
        return "certificate"
    if "project" in filename:
        return "project"
    if "note" in filename:
        return "notes"
    if "resume" in filename:
        return "resume"
    return "unknown"


# ==========================================================
# Read PDFs
# ==========================================================
def load_documents(document_folder):
    all_pages_data = []
    parent_documents = []
    parent_id = 0
    pdf_files = []
    for file in os.listdir(document_folder):
        if file.endswith(".pdf"):
            pdf_files.append(os.path.join(document_folder, file))
    logger.info("Found %d PDF documents", len(pdf_files))

    for pdf_path in pdf_files:
        reader = PdfReader(pdf_path)
        source_file = os.path.basename(pdf_path)
        document_type = infer_document_type(source_file)
        logger.info("Loading %s", source_file)
        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            if text:
                parent_documents.append(
                    {
                        "parent_id": parent_id,
                        "source_file": source_file,
                        "document_type": document_type,
                        "page_number": page_num,
                        "text": text,
                    }
                )
                all_pages_data.append(
                    {
                        "parent_id": parent_id,
                        "source_file": source_file,
                        "document_type": document_type,
                        "page_number": page_num,
                        "text": text,
                    }
                )
                parent_id += 1
    logger.info("Loaded %d pages", len(all_pages_data))
    return (all_pages_data, parent_documents)


# ==========================================================
# Chunking
# ==========================================================
def chunk_text_with_metadata(pages_data, chunk_size, overlap):
    chunks = []
    chunk_id = 0
    for page in pages_data:
        text = page["text"]
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]
            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "parent_id": page["parent_id"],
                    "source_file": page["source_file"],
                    "document_type": page["document_type"],
                    "page_number": page["page_number"],
                    "start_pos": start,
                    "end_pos": min(end, len(text)),
                    "text": chunk_text,
                }
            )
            chunk_id += 1
            start += chunk_size - overlap
    logger.info("Created %d chunks", len(chunks))
    return chunks
