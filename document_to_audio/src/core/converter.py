"""
Core document to audio conversion functionality.
"""
import os
from datetime import datetime
from ..utils import document_utils, audio_utils
from ..utils.storage.local_storage import LocalStorage
from ..services.google_services import GoogleServices

class DocumentToAudio:
    def __init__(self, storage_dir=None, use_google_services=False):
        """
        Initialize the converter
        Args:
            storage_dir: Custom storage directory for audio files
            use_google_services: Whether to enable Google Services integration
        """
        self.storage = LocalStorage(storage_dir)
        self.google_services = GoogleServices() if use_google_services else None

    def process_document(self, input_path, output_path=None, language='en', 
                        is_google_doc=False, save_to_drive=False):
        """Process document and convert to audio"""
        # Extract text based on input type
        if is_google_doc:
            if not self.google_services:
                raise ValueError("Google Services not enabled. Initialize with use_google_services=True")
            try:
                doc_id = document_utils.get_google_doc_id_from_url(input_path)
                docs_service = self.google_services.get_docs_service()
                text = document_utils.extract_text_from_google_doc(docs_service, doc_id)
            except Exception as e:
                raise ValueError(f"Error processing Google Doc: {str(e)}")
        else:
            # Handle local files
            if input_path.lower().endswith('.pdf'):
                text = document_utils.extract_text_from_pdf(input_path)
            elif input_path.lower().endswith('.docx'):
                text = document_utils.extract_text_from_docx(input_path)
            else:
                raise ValueError("Unsupported file format. Please use PDF, DOCX, or Google Docs URL.")

        # Generate temporary output path if not provided
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if is_google_doc:
                doc_id = document_utils.get_google_doc_id_from_url(input_path)
                output_path = f"google_doc_{doc_id}_{timestamp}.mp3"
            else:
                base_name = os.path.splitext(os.path.basename(input_path))[0]
                output_path = f"{base_name}_{timestamp}.mp3"

        # Convert to audio
        temp_audio_path = audio_utils.convert_text_to_audio(text, output_path, language)

        # Save to local storage
        doc_type = 'google_docs' if is_google_doc else os.path.splitext(input_path)[1][1:]
        stored_path = self.storage.save_file(
            temp_audio_path,
            original_doc_path=input_path,
            doc_type=doc_type
        )

        # Clean up temporary file if it's different from the stored path
        if temp_audio_path != stored_path and os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

        result = {
            'audio_path': stored_path,
            'original_document': input_path,
            'metadata': self.storage.get_file_info(stored_path)
        }

        # Optionally upload to Google Drive
        if save_to_drive and self.google_services:
            file_id = self.google_services.upload_file(
                stored_path,
                os.path.basename(stored_path)
            )
            result['drive_file_id'] = file_id

        return result
