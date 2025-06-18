"""
Document processing utilities for different file formats.
"""
from PyPDF2 import PdfReader
from docx import Document

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    text = ""
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(docx_path):
    """Extract text from DOCX file"""
    doc = Document(docx_path)
    return " ".join([paragraph.text for paragraph in doc.paragraphs])

def extract_text_from_google_doc(service, doc_id):
    """Extract text from Google Doc using its ID"""
    doc = service.documents().get(documentId=doc_id).execute()
    
    text = ''
    for content in doc.get('body').get('content'):
        if 'paragraph' in content:
            for element in content.get('paragraph').get('elements'):
                if 'textRun' in element:
                    text += element.get('textRun').get('content')
    
    return text

def get_google_doc_id_from_url(url):
    """Extract Google Doc ID from URL"""
    if '/document/d/' in url:
        doc_id = url.split('/document/d/')[1].split('/')[0]
    elif '/spreadsheets/d/' in url:
        raise ValueError("This is a Google Sheets URL. Please provide a Google Docs URL.")
    else:
        raise ValueError("Invalid Google Docs URL format.")
    return doc_id
