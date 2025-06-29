import logging
from docling.document_converter import DocumentConverter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Docling once
converter = DocumentConverter()

def convert_contract(file_path):
    """
    Converts a PDF or DOCX contract to markdown
    """
    try:
        result = converter.convert(file_path)
        markdown_text = result.document.export_to_markdown()
        logger.info(f"Converted {file_path} to markdown successfully.")
        return markdown_text
    except Exception as e:
        logger.error(f"Docling conversion failed: {e}")
        return None
