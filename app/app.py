from resume_file_reader import ResumeFileReader
from resume_summary import ResumeSummary
import logging

class App:

    def __init__(self, resume_file, logging):
        self.logging = logging
        self.resume_file = resume_file

    def process_resume(self):
        try:
            rfr = ResumeFileReader(self.resume_file, self.logging)
            resume_data = rfr.extract_text_from_file()
            self.logging.info(f"Extracted resume data {resume_data}")

            rfs = ResumeSummary(resume_data,self.logging)
            rfs.generate_resume_summary()
        except Exception as e:
            self.logging.error(f"Unable to process the resume {self.resume_file}")




if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.DEBUG)
    resume_file =  "../data/raw/resume.pdf"
    app = App(resume_file, logging)
