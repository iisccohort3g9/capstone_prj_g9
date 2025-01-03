import PyPDF2
from docx import Document
import os
import time
# import logging
from clearml import Task, Logger

class ResumeFileReader:

    def __init__(self, file_path, logger=None):
        self.file_path = file_path
        self.logger = logger or Logger.current_logger()

    def extract_text_from_pdf(self):
        """Extract text from a PDF file."""
        start_time = time.time()
        text = ""
        with open(self.file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        end_time = time.time()

        # Report processing time as a scalar metric
        processing_time = end_time - start_time

        self.logger.report_scalar(
            title="Text Extraction Metrics",
            series="PDF Processing Time",
            value=processing_time,
            iteration=1  # You could change this to represent different steps or epochs
        )

        if self.logger:
            self.logger.report_text(f"Text extracted in {processing_time} seconds")
        return text

    def extract_text_from_docx(self):
        """Extract text from a DOCX file."""
        document = Document(self.file_path)
        text = ""
        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"
        if self.logger:
            self.logger.report_text(f"Text extracted {text}")
        return text

    def extract_text_from_file(self):
        """Extract text from a PDF or DOCX file based on the file extension."""
        ext = os.path.splitext(self.file_path)[1].lower()
        if ext == '.pdf':
            return self.extract_text_from_pdf()
        elif ext == '.docx':
            return self.extract_text_from_docx()
        else:
            raise ValueError("Unsupported file format. Use PDF or DOCX.")