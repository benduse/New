"""
Unit tests for Google services.
"""
import pytest
from document_to_audio.src.services.google_services import GoogleServices
from unittest.mock import patch, MagicMock

def test_google_services_initialization():
    """Test GoogleServices initialization"""
    service = GoogleServices()
    assert service.SCOPES is not None
    assert len(service.SCOPES) > 0
    assert service.credentials is None

def test_authentication(mock_credentials):
    """Test Google authentication"""
    service = GoogleServices()
    
    with patch('google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file') as mock_flow:
        mock_creds = MagicMock()
        mock_creds.valid = True
        mock_flow.return_value.run_local_server.return_value = mock_creds
        
        credentials = service.authenticate()
        assert credentials is not None
        assert credentials.valid

def test_get_drive_service(mock_google_services):
    """Test getting Google Drive service"""
    service = mock_google_services
    drive_service = service.get_drive_service()
    assert drive_service is not None

    # Test file upload
    file_id = service.upload_file("test_file.txt", "test_file.txt")
    assert file_id == "mock_file_id"

def test_get_docs_service(mock_google_services):
    """Test getting Google Docs service"""
    service = mock_google_services
    docs_service = service.get_docs_service()
    assert docs_service is not None
    
    # Verify the service can get document content
    doc = docs_service.documents().get(documentId="test_id").execute()
    assert "content" in doc["body"]
