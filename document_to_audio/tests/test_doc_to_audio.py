import os
import pytest
from playwright.sync_api import expect
from ..doc_to_audio import DocumentToAudio
import tempfile
from unittest.mock import patch, MagicMock
from google.oauth2.credentials import Credentials

def test_pdf_to_audio(sample_pdf, temp_dir):
    """Test converting a PDF file to audio"""
    converter = DocumentToAudio()
    output_path = os.path.join(temp_dir, "output.mp3")
    
    with patch('googleapiclient.discovery.build') as mock_build:
        # Mock the Drive API response
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_service.files.return_value.create.return_value.execute.return_value = {'id': 'mock_file_id'}
        
        result = converter.process_document(
            input_path=sample_pdf,
            output_path=output_path
        )
        
        assert os.path.exists(result['audio_path'])
        assert result['drive_file_id'] == 'mock_file_id'
        
        # Check if the audio file was created with content
        assert os.path.getsize(result['audio_path']) > 0

def test_docx_to_audio(sample_docx, temp_dir):
    """Test converting a DOCX file to audio"""
    converter = DocumentToAudio()
    output_path = os.path.join(temp_dir, "output.mp3")
    
    with patch('googleapiclient.discovery.build') as mock_build:
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_service.files.return_value.create.return_value.execute.return_value = {'id': 'mock_file_id'}
        
        result = converter.process_document(
            input_path=sample_docx,
            output_path=output_path
        )
        
        assert os.path.exists(result['audio_path'])
        assert result['drive_file_id'] == 'mock_file_id'
        assert os.path.getsize(result['audio_path']) > 0

@pytest.mark.asyncio
async def test_google_docs_to_audio(mock_credentials, temp_dir, page):
    """Test converting a Google Doc to audio using Playwright"""
    converter = DocumentToAudio()
    
    # Mock Google OAuth flow
    with patch('google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file') as mock_flow:
        mock_credentials = MagicMock(spec=Credentials)
        mock_credentials.valid = True
        mock_flow.return_value.run_local_server.return_value = mock_credentials
        
        # Mock Google Docs API
        with patch('googleapiclient.discovery.build') as mock_build:
            mock_docs_service = MagicMock()
            mock_drive_service = MagicMock()
            
            def mock_build_service(service, *args, **kwargs):
                if service == 'docs':
                    return mock_docs_service
                return mock_drive_service
            
            mock_build.side_effect = mock_build_service
            
            # Mock Docs API response
            mock_docs_service.documents.return_value.get.return_value.execute.return_value = {
                'body': {
                    'content': [{
                        'paragraph': {
                            'elements': [{
                                'textRun': {
                                    'content': 'This is a test Google Doc.'
                                }
                            }]
                        }
                    }]
                }
            }
            
            # Mock Drive API response
            mock_drive_service.files.return_value.create.return_value.execute.return_value = {
                'id': 'mock_drive_file_id'
            }
            
            result = converter.process_document(
                input_path='https://docs.google.com/document/d/test_doc_id/edit',
                output_path=os.path.join(temp_dir, "output.mp3"),
                is_google_doc=True
            )
            
            assert os.path.exists(result['audio_path'])
            assert result['drive_file_id'] == 'mock_drive_file_id'
            assert os.path.getsize(result['audio_path']) > 0

def test_invalid_file_format():
    """Test handling of invalid file formats"""
    converter = DocumentToAudio()
    
    with pytest.raises(ValueError) as exc_info:
        converter.process_document('invalid.txt')
    
    assert "Unsupported file format" in str(exc_info.value)

def test_invalid_google_doc_url():
    """Test handling of invalid Google Doc URLs"""
    converter = DocumentToAudio()
    
    with pytest.raises(ValueError) as exc_info:
        converter.process_document(
            'https://invalid-url.com',
            is_google_doc=True
        )
    
    assert "Invalid Google Docs URL format" in str(exc_info.value)

@pytest.mark.asyncio
async def test_google_docs_authentication(page):
    """Test Google Docs authentication flow using Playwright"""
    converter = DocumentToAudio()
    
    with patch('google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file') as mock_flow:
        # Mock the authentication flow
        mock_credentials = MagicMock(spec=Credentials)
        mock_credentials.valid = True
        mock_flow.return_value.run_local_server.return_value = mock_credentials
        
        # Simulate authentication
        service = converter.authenticate_google_drive()
        
        assert service is not None
        mock_flow.assert_called_once()

def test_large_document_handling(temp_dir):
    """Test handling of large documents"""
    converter = DocumentToAudio()
    
    # Create a large test document
    with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as f:
        doc = Document()
        # Add 100 paragraphs
        for i in range(100):
            doc.add_paragraph(f"This is test paragraph {i}.")
        doc.save(f.name)
        
        with patch('googleapiclient.discovery.build') as mock_build:
            mock_service = MagicMock()
            mock_build.return_value = mock_service
            mock_service.files.return_value.create.return_value.execute.return_value = {'id': 'mock_file_id'}
            
            result = converter.process_document(
                input_path=f.name,
                output_path=os.path.join(temp_dir, "large_output.mp3")
            )
            
            assert os.path.exists(result['audio_path'])
            assert os.path.getsize(result['audio_path']) > 0
    
    os.unlink(f.name)
