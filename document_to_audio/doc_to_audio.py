import os
from gtts import gTTS
from PyPDF2 import PdfReader
from docx import Document
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle

class DocumentToAudio:
    def __init__(self):
        self.SCOPES = [
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/docs.readonly',
            'https://www.googleapis.com/auth/drive.readonly'
        ]
        self.credentials = None

    def authenticate_google_drive(self):
        """Authenticate with Google Drive"""
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.credentials = pickle.load(token)
        
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                self.credentials = flow.run_local_server(port=0)
            
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.credentials, token)

        return build('drive', 'v3', credentials=self.credentials)

    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF file"""
        text = ""
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text()
        return text

    def extract_text_from_docx(self, docx_path):
        """Extract text from DOCX file"""
        doc = Document(docx_path)
        return " ".join([paragraph.text for paragraph in doc.paragraphs])

    def convert_text_to_audio(self, text, output_path, language='en'):
        """Convert text to audio using gTTS"""
        tts = gTTS(text=text, lang=language)
        tts.save(output_path)
        return output_path

    def upload_to_drive(self, file_path, file_name):
        """Upload file to Google Drive"""
        service = self.authenticate_google_drive()
        file_metadata = {'name': file_name}
        media = MediaFileUpload(file_path, resumable=True)
        file = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
        return file.get('id')

    def extract_text_from_google_doc(self, doc_id):
        """Extract text from Google Doc using its ID"""
        service = build('docs', 'v1', credentials=self.credentials)
        doc = service.documents().get(documentId=doc_id).execute()
        
        text = ''
        for content in doc.get('body').get('content'):
            if 'paragraph' in content:
                for element in content.get('paragraph').get('elements'):
                    if 'textRun' in element:
                        text += element.get('textRun').get('content')
        
        return text

    def get_google_doc_id_from_url(self, url):
        """Extract Google Doc ID from URL"""
        # Handle different URL formats
        if '/document/d/' in url:
            doc_id = url.split('/document/d/')[1].split('/')[0]
        elif '/spreadsheets/d/' in url:
            raise ValueError("This is a Google Sheets URL. Please provide a Google Docs URL.")
        else:
            raise ValueError("Invalid Google Docs URL format.")
        return doc_id

    def process_document(self, input_path, output_path=None, language='en'):
        """Process document and convert to audio"""
        # Determine file type and extract text
        if input_path.lower().endswith('.pdf'):
            text = self.extract_text_from_pdf(input_path)
        elif input_path.lower().endswith('.docx'):
            text = self.extract_text_from_docx(input_path)
        elif '/document/d/' in input_path:  # Check if it's a Google Docs URL
            doc_id = self.get_google_doc_id_from_url(input_path)
            text = self.extract_text_from_google_doc(doc_id)
        else:
            raise ValueError("Unsupported file format. Please use PDF, DOCX, or Google Docs URL.")

        # Generate output path if not provided
        if output_path is None:
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            output_path = f"{base_name}.mp3"

        # Convert to audio
        audio_path = self.convert_text_to_audio(text, output_path, language)

        # Upload to Google Drive
        file_id = self.upload_to_drive(audio_path, os.path.basename(output_path))
        
        return {
            'audio_path': audio_path,
            'drive_file_id': file_id
        }

def main():
    converter = DocumentToAudio()
    
    # Example usage
    try:
        result = converter.process_document(
            input_path='example.pdf',  # Replace with your document path
            output_path='output.mp3',  # Optional: specify output path
            language='en'  # Optional: specify language
        )
        print(f"Audio file created at: {result['audio_path']}")
        print(f"Uploaded to Google Drive with ID: {result['drive_file_id']}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
