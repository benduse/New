"""
Unit tests for document utilities.
"""
import pytest
from document_to_audio.src.utils import document_utils

def test_extract_text_from_pdf(sample_pdf, sample_text):
    """Test PDF text extraction"""
    extracted_text = document_utils.extract_text_from_pdf(sample_pdf)
    assert sample_text in extracted_text

def test_extract_text_from_docx(sample_docx, sample_text):
    """Test DOCX text extraction"""
    extracted_text = document_utils.extract_text_from_docx(sample_docx)
    assert sample_text in extracted_text

def test_get_google_doc_id_from_url():
    """Test Google Doc ID extraction from URL"""
    # Test valid URL
    url = "https://docs.google.com/document/d/1234567890abcdef/edit"
    doc_id = document_utils.get_google_doc_id_from_url(url)
    assert doc_id == "1234567890abcdef"

    # Test invalid URL
    with pytest.raises(ValueError) as exc_info:
        document_utils.get_google_doc_id_from_url("https://invalid-url.com")
    assert "Invalid Google Docs URL format" in str(exc_info.value)

    # Test Google Sheets URL
    with pytest.raises(ValueError) as exc_info:
        document_utils.get_google_doc_id_from_url("https://docs.google.com/spreadsheets/d/123/edit")
    assert "Google Sheets URL" in str(exc_info.value)

def test_extract_text_from_google_doc(mock_google_services):
    """Test Google Doc text extraction"""
    service = mock_google_services.get_docs_service()
    text = document_utils.extract_text_from_google_doc(service, "test_doc_id")
    assert "This is a test Google Doc." in text
