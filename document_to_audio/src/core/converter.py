"""
Core document to audio conversion functionality.
"""
import os
from ..utils import document_utils, audio_utils
from ..services.google_services import GoogleServices

class DocumentToAudio:
    def __init__(self):
        self.google_services = GoogleServices()

    def process_document(self, input_path, output_path=None, language='en', is_google_doc=False):
        """Process document and convert to audio"""
        # Extract text based on input type
        if is_google_doc:
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

        # Generate output path if not provided
        if output_path is None:
            if is_google_doc:
                doc_id = document_utils.get_google_doc_id_from_url(input_path)
                output_path = f"google_doc_{doc_id}.mp3"
            else:
                base_name = os.path.splitext(os.path.basename(input_path))[0]
                output_path = f"{base_name}.mp3"

        # Convert to audio
        audio_path = audio_utils.convert_text_to_audio(text, output_path, language)

        # Upload to Google Drive
        file_id = self.google_services.upload_file(audio_path, os.path.basename(output_path))
        
        return {
            'audio_path': audio_path,
            'drive_file_id': file_id
        }
