"""
Local storage utilities for audio files.
"""
import os
import shutil
from datetime import datetime
from pathlib import Path

class LocalStorage:
    def __init__(self, base_dir=None):
        """Initialize local storage with a base directory"""
        if base_dir is None:
            # Default to user's home directory/Documents/audio_documents
            base_dir = os.path.join(str(Path.home()), "Documents", "audio_documents")
        
        self.base_dir = base_dir
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        """Create storage directory if it doesn't exist"""
        os.makedirs(self.base_dir, exist_ok=True)
        # Create subdirectories for organization
        for subdir in ['pdf', 'docx', 'google_docs', 'other']:
            os.makedirs(os.path.join(self.base_dir, subdir), exist_ok=True)

    def _get_storage_path(self, filename, doc_type):
        """Get the appropriate storage path based on document type"""
        # Create a directory structure: type/year/month/
        now = datetime.now()
        year_month = now.strftime("%Y/%m")
        storage_path = os.path.join(self.base_dir, doc_type, year_month)
        os.makedirs(storage_path, exist_ok=True)
        return os.path.join(storage_path, filename)

    def save_file(self, file_path, original_doc_path=None, doc_type=None):
        """
        Save a file to local storage with organized structure
        Returns the new file path
        """
        # Determine document type
        if doc_type is None:
            if original_doc_path:
                ext = os.path.splitext(original_doc_path)[1].lower()
                if ext == '.pdf':
                    doc_type = 'pdf'
                elif ext == '.docx':
                    doc_type = 'docx'
                else:
                    doc_type = 'other'
            else:
                doc_type = 'other'

        # Generate filename if it doesn't exist
        filename = os.path.basename(file_path)
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"audio_{timestamp}.mp3"

        # Get storage path
        storage_path = self._get_storage_path(filename, doc_type)
        
        # Copy file to storage
        shutil.copy2(file_path, storage_path)
        
        # Create metadata file
        metadata_path = storage_path + '.meta'
        with open(metadata_path, 'w') as f:
            f.write(f"Original Document: {original_doc_path}\n")
            f.write(f"Creation Date: {datetime.now().isoformat()}\n")
            f.write(f"Document Type: {doc_type}\n")

        return storage_path

    def list_files(self, doc_type=None):
        """List all audio files in storage, optionally filtered by document type"""
        files = []
        search_dir = self.base_dir if doc_type is None else os.path.join(self.base_dir, doc_type)
        
        for root, _, filenames in os.walk(search_dir):
            for filename in filenames:
                if filename.endswith('.mp3'):
                    files.append(os.path.join(root, filename))
        
        return files

    def get_file_info(self, file_path):
        """Get metadata for a stored file"""
        metadata_path = file_path + '.meta'
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                return dict(line.strip().split(': ', 1) for line in f.readlines())
        return None
