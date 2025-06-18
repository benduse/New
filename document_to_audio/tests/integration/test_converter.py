"""
Integration tests for the DocumentToAudio converter.
"""
import os
import pytest
from document_to_audio.src.core.converter import DocumentToAudio
from unittest.mock import patch

@pytest.mark.integration
def test_pdf_conversion_workflow(sample_pdf, temp_dir, mock_google_services):
    """Test complete PDF to audio conversion workflow"""
    with patch('document_to_audio.src.core.converter.GoogleServices') as mock_gs:
        mock_gs.return_value = mock_google_services
        
        converter = DocumentToAudio()
        output_path = os.path.join(temp_dir, "output.mp3")
        
        result = converter.process_document(
            input_path=sample_pdf,
            output_path=output_path
        )
        
        assert os.path.exists(result['audio_path'])
        assert result['drive_file_id'] == 'mock_file_id'
        assert os.path.getsize(result['audio_path']) > 0

@pytest.mark.integration
def test_docx_conversion_workflow(sample_docx, temp_dir, mock_google_services):
    """Test complete DOCX to audio conversion workflow"""
    with patch('document_to_audio.src.core.converter.GoogleServices') as mock_gs:
        mock_gs.return_value = mock_google_services
        
        converter = DocumentToAudio()
        output_path = os.path.join(temp_dir, "output.mp3")
        
        result = converter.process_document(
            input_path=sample_docx,
            output_path=output_path
        )
        
        assert os.path.exists(result['audio_path'])
        assert result['drive_file_id'] == 'mock_file_id'
        assert os.path.getsize(result['audio_path']) > 0

@pytest.mark.integration
def test_google_doc_conversion_workflow(temp_dir, mock_google_services):
    """Test complete Google Doc to audio conversion workflow"""
    with patch('document_to_audio.src.core.converter.GoogleServices') as mock_gs:
        mock_gs.return_value = mock_google_services
        
        converter = DocumentToAudio()
        output_path = os.path.join(temp_dir, "output.mp3")
        
        result = converter.process_document(
            input_path='https://docs.google.com/document/d/test_doc_id/edit',
            output_path=output_path,
            is_google_doc=True
        )
        
        assert os.path.exists(result['audio_path'])
        assert result['drive_file_id'] == 'mock_file_id'
        assert os.path.getsize(result['audio_path']) > 0

@pytest.mark.integration
def test_error_handling(mock_google_services):
    """Test error handling in the conversion workflow"""
    with patch('document_to_audio.src.core.converter.GoogleServices') as mock_gs:
        mock_gs.return_value = mock_google_services
        
        converter = DocumentToAudio()
        
        # Test invalid file format
        with pytest.raises(ValueError) as exc_info:
            converter.process_document('invalid.txt')
        assert "Unsupported file format" in str(exc_info.value)
        
        # Test invalid Google Doc URL
        with pytest.raises(ValueError) as exc_info:
            converter.process_document(
                'https://invalid-url.com',
                is_google_doc=True
            )
        assert "Invalid Google Docs URL format" in str(exc_info.value)
