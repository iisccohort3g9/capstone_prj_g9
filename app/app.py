from resume_file_reader import ResumeFileReader
from resume_summary import ResumeSummary
import logging
from clearml import Task
from langchain_community.callbacks import ClearMLCallbackHandler
from langchain_core.callbacks import StdOutCallbackHandler

class App:

    def __init__(self, resume_file, logging):
        self.logging = logging
        self.resume_file = resume_file
        # Initialize ClearML Task
        self.task = Task.init(
            project_name="Resume Summary AV Generation",
            task_name="Generate Resume Summary",
            task_type=Task.TaskTypes.data_processing
        )
        # Set up ClearML Callback Handler
        self.callback_handler = ClearMLCallbackHandler(
            task_type="inference",
            project_name="Resume Summary AV Generation",
            task_name="Generate Resume Summary",
            tags=["test"],
            # Change the following parameters based on the amount of detail you want tracked
            visualize=True,
            complexity_metrics=False,
            stream_logs=True
        )
        self.callbacks = (StdOutCallbackHandler(), self.callback_handler)
        # Connect parameters to task
        self.parameters = {"resume_file": resume_file}
        self.task.connect(self.parameters)

    def process_resume(self):
        try:
            rfr = ResumeFileReader(self.resume_file, self.logging, callbacks=self.callbacks)
            resume_data = rfr.extract_text_from_file()
            self.logging.info(f"Extracted resume data {resume_data}")

            rfs = ResumeSummary(resume_data,self.logging, callbacks=self.callbacks)
            rfs.generate_resume_summary()
        except Exception as e:
            self.logging.error(f"Unable to process the resume {self.resume_file}")

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.DEBUG)
    resume_file =  "../data/raw/Soumen Ghosh.pdf"
    app = App(resume_file, logging)
    # Process the resume and generate summary
    # app.process_resume()
    
    # After processing, flush the tracker to clear any pending updates to ClearML
    # app.flush_tracker()
