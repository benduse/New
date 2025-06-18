"""
Google services authentication and interaction module.
"""
import os
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class GoogleServices:
    def __init__(self, scopes=None):
        self.SCOPES = scopes or [
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/docs.readonly',
            'https://www.googleapis.com/auth/drive.readonly'
        ]
        self.credentials = None

    def authenticate(self):
        """Authenticate with Google services"""
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

        return self.credentials

    def get_drive_service(self):
        """Get Google Drive service"""
        if not self.credentials:
            self.authenticate()
        return build('drive', 'v3', credentials=self.credentials)

    def get_docs_service(self):
        """Get Google Docs service"""
        if not self.credentials:
            self.authenticate()
        return build('docs', 'v1', credentials=self.credentials)

    def upload_file(self, file_path, file_name):
        """Upload file to Google Drive"""
        service = self.get_drive_service()
        file_metadata = {'name': file_name}
        media = MediaFileUpload(file_path, resumable=True)
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        return file.get('id')
