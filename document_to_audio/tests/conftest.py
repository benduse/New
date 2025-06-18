"""
Test fixtures for the document_to_audio package.
"""
import os
import json
import pytest
import tempfile
from pathlib import Path
from unittest.mock import MagicMock
from google.oauth2.credentials import Credentials

@pytest.fixture
def sample_text():
    """Sample text for testing"""
    return "This is a test document for audio conversion."

@pytest.fixture
def sample_pdf(sample_text):
    """Create a sample PDF file for testing"""
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        from reportlab.pdfgen import canvas
        c = canvas.Canvas(f.name)
        c.drawString(100, 750, sample_text)
        c.save()
        yield f.name
    os.unlink(f.name)

@pytest.fixture
def sample_docx(sample_text):
    """Create a sample DOCX file for testing"""
    from docx import Document
    with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as f:
        doc = Document()
        doc.add_paragraph(sample_text)
        doc.save(f.name)
        yield f.name
    os.unlink(f.name)

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test outputs"""
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

@pytest.fixture
def mock_credentials():
    """Mock Google credentials for testing"""
    creds_path = Path('tests/mock_credentials.json')
    creds_path.parent.mkdir(exist_ok=True)
    
    mock_creds = {
        "installed": {
            "client_id": "mock_client_id",
            "client_secret": "mock_secret",
            "redirect_uris": ["http://localhost"]
        }
    }
    
    with open(creds_path, 'w') as f:
        json.dump(mock_creds, f)
    
    yield str(creds_path)
    
    if creds_path.exists():
        creds_path.unlink()

@pytest.fixture
def mock_google_services():
    """Mock Google Services for testing"""
    class MockGoogleServices:
        def __init__(self):
            self.credentials = MagicMock(spec=Credentials)
            self.credentials.valid = True

        def authenticate(self):
            return self.credentials

        def get_drive_service(self):
            service = MagicMock()
            service.files.return_value.create.return_value.execute.return_value = {
                'id': 'mock_file_id'
            }
            return service

        def get_docs_service(self):
            service = MagicMock()
            service.documents.return_value.get.return_value.execute.return_value = {
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
            return service

        def upload_file(self, file_path, file_name):
            return 'mock_file_id'

    return MockGoogleServices()
