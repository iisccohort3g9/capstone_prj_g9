import PyPDF2
from docx import Document
import os
import logging

class ResumeFileReader:

    def __init__(self, file_path, logging):
        self.file_path = file_path
        self.logging = logging

    def extract_text_from_pdf(self):
        """Extract text from a PDF file."""
        text = ""
        with open(self.file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        self.logging.info(f"Text extracted {text}")
        return text

    def extract_text_from_docx(self):
        """Extract text from a DOCX file."""
        document = Document(self.file_path)
        text = ""
        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"
        self.logging.info(f"Text extracted {text}")
        return text

    def extract_text_from_file(self):
        """Extract text from a PDF or DOCX file based on the file extension."""
        ext = os.path.splitext(self.file_path)[1].lower()
        if ext == '.pdf':
            return self.extract_text_from_pdf(self.file_path)
        elif ext == '.docx':
            return self.extract_text_from_docx(self.file_path)
        else:
            raise ValueError("Unsupported file format. Use PDF or DOCX.")