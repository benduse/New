# Document to Audio Converter

A powerful Python tool that converts various document formats to audio files and automatically saves them to Google Drive. This tool supports local PDF and DOCX files, as well as Google Docs documents.

## Features

### Document Support
- **PDF Files**: Convert any readable PDF document to audio
- **DOCX Files**: Convert Microsoft Word documents to audio
- **Google Docs**: Direct integration with Google Docs for online documents
- **Text Extraction**: Intelligent text extraction maintaining document structure

### Audio Conversion
- **Multiple Languages**: Support for multiple languages using Google Text-to-Speech (gTTS)
- **Custom Output**: Configurable output paths and filenames
- **Quality Control**: High-quality audio output with natural-sounding speech
- **Format**: MP3 output format for wide compatibility

### Google Integration
- **Google Drive Upload**: Automatic upload of generated audio files to Google Drive
- **Google Docs Access**: Direct access to Google Docs without downloading
- **Authentication**: Secure OAuth2 authentication for Google services
- **File Management**: Organized file storage in Google Drive

### Error Handling
- Robust error handling for file operations
- Clear error messages for troubleshooting
- Graceful handling of network issues
- Validation of input documents and formats

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd document-to-audio
```

2. Install dependencies using conda:
```bash
conda env update -f environment.yml
```

3. Set up Google Cloud Project:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project
   - Enable the required APIs:
     - Google Drive API
     - Google Docs API
   - Create OAuth 2.0 credentials
   - Download credentials and save as `credentials.json` in the project directory

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

## With Local Files
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

## With Google Docs
```python
from doc_to_audio import DocumentToAudio

converter = DocumentToAudio()
result = converter.process_document(
    input_path='https://docs.google.com/document/d/YOUR_DOC_ID/edit',
    language='en',  # Optional, defaults to English
    is_google_doc=True  # Important: set this to True for Google Docs
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

## Limitations

### Document Processing
- PDF files must have extractable text (scanned PDFs not supported)
- Complex document layouts may affect text extraction order
- Tables and diagrams are processed as text only
- Maximum file size: 100MB for local files, 50MB for Google Docs

### Audio Conversion
- Maximum text length: 100,000 characters per conversion
- Audio quality depends on gTTS service
- Network connection required for text-to-speech conversion
- Processing time increases with document length

### Google Services
- Requires internet connection
- Google account and API setup required
- API quotas and limitations apply
- OAuth2 credentials must be maintained

### Performance
- Large documents may take significant processing time
- Concurrent processing limited by API quotas
- Memory usage scales with document size
- Network speed affects conversion time

## Development

### Running Tests
```bash
# Run all tests
pytest tests/

# Run unit tests only
pytest tests/unit/

# Run integration tests
pytest tests/integration/
```

### Project Structure
```
document_to_audio/
├── src/
│   ├── core/           # Main conversion logic
│   ├── services/       # External service integrations
│   └── utils/          # Helper functions
├── tests/
│   ├── unit/          # Unit tests
│   └── integration/   # Integration tests
└── docs/              # Documentation
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Write tests for new features
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Cloud Platform for APIs
- gTTS for text-to-speech conversion
- PyPDF2 for PDF processing
- python-docx for DOCX processing

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify credentials.json is properly configured
   - Check Google Cloud Console API enablement
   - Ensure proper OAuth2 scopes

2. **File Processing Errors**
   - Verify file format compatibility
   - Check file permissions
   - Ensure file is not corrupted

3. **Network Issues**
   - Check internet connection
   - Verify API quotas
   - Check firewall settings

4. **Audio Output Issues**
   - Verify supported language code
   - Check available disk space
   - Ensure write permissions

### Support

For issues and feature requests, please use the GitHub issue tracker.
