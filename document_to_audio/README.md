# Document to Audio Converter

This script converts PDF and DOCX documents to audio files and automatically uploads them to Google Drive.

## Features

- Supports PDF and DOCX file formats
- Converts text to speech using Google Text-to-Speech (gTTS)
- Automatically uploads generated audio files to Google Drive
- Supports multiple languages

## Prerequisites

1. Python 3.x
2. Required packages (install using conda/pip):
   - gTTS
   - PyPDF2
   - python-docx
   - google-auth-oauthlib
   - google-auth-httplib2
   - google-api-python-client

## Setup

1. Clone this repository
2. Install required packages:
   ```bash
   conda env update -f environment.yml
   ```
3. Set up Google Drive API:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable the Google Drive API
   - Create credentials (OAuth 2.0 Client ID)
   - Download the credentials and save as `credentials.json` in the project directory

## Usage

```python
from doc_to_audio import DocumentToAudio

converter = DocumentToAudio()
result = converter.process_document(
    input_path='path/to/your/document.pdf',
    output_path='output.mp3',  # Optional
    language='en'  # Optional, defaults to English
)

print(f"Audio file created at: {result['audio_path']}")
print(f"Uploaded to Google Drive with ID: {result['drive_file_id']}")
```

## Supported Languages

The script supports all languages available in gTTS. Common languages include:
- 'en' (English)
- 'es' (Spanish)
- 'fr' (French)
- 'de' (German)
- 'it' (Italian)
- 'pt' (Portuguese)

## Error Handling

The script includes error handling for:
- Unsupported file formats
- File read/write errors
- Google Drive API authentication errors
- Text-to-speech conversion errors

## Notes

- Large documents may take longer to process
- Audio files are temporarily stored locally before being uploaded to Google Drive
- Make sure you have sufficient Google Drive storage space
- The first time you run the script, it will open a browser window for Google authentication
