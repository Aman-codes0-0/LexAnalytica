"""
Text extraction module for legal documents.
Supports PDF, DOCX, and TXT file formats.
"""

import os
from PyPDF2 import PdfReader
from docx import Document


def extract_text(file_path: str) -> str:
    """
    Extract raw text from a legal document.
    
    Args:
        file_path: Path to the uploaded document file.
    
    Returns:
        Extracted raw text as a string.
    
    Raises:
        ValueError: If the file format is not supported.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return _extract_from_pdf(file_path)
    elif ext == ".docx":
        return _extract_from_docx(file_path)
    elif ext == ".txt":
        return _extract_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}. Supported formats: PDF, DOCX, TXT")


def _extract_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file using PyPDF2."""
    reader = PdfReader(file_path)
    pages_text = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages_text.append(text.strip())
    return "\n\n".join(pages_text)


def _extract_from_docx(file_path: str) -> str:
    """Extract text from a DOCX file using python-docx."""
    doc = Document(file_path)
    paragraphs = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
    return "\n\n".join(paragraphs)


def _extract_from_txt(file_path: str) -> str:
    """Extract text from a plain text file."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().strip()
