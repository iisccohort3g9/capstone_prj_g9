from resume_file_reader import ResumeFileReader
from resume_summary import ResumeSummary
import logging
from clearml import Task, Logger
from langchain_community.callbacks import ClearMLCallbackHandler
from langchain_core.callbacks import StdOutCallbackHandler

class App:

    def __init__(self, resume_file, python_logger, logger=None):
        self.python_logger = python_logger
        self.resume_file = resume_file
        # Initialize ClearML Task
        self.task = Task.init(
            project_name="Resume Summary AV Generation",
            task_name="Generate Resume Summary",
            task_type=Task.TaskTypes.data_processing
        )
        # Initialize ClearML Logger
        self.logger = logger or Logger.current_logger()
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
            rfr = ResumeFileReader(self.resume_file, self.logger)
            resume_data = rfr.extract_text_from_file()
            self.python_logger.info(f"Extracted resume data {resume_data}")
            # if self.logger:
            #     self.logger.report_text(f"Extracted resume data {resume_data}")

            rfs = ResumeSummary(resume_data,self.logger, callbacks=self.callbacks)
            rfs.generate_resume_summary()
        except Exception as e:
            self.python_logger.error(f"Unable to process the resume {self.resume_file}")
            # if self.logger:
            #     self.logger.report_text(f"Unable to process the resume {self.resume_file}")
            # print(f"Error: {str(e)}")

if __name__ == "__main__":
    python_logger = logging.getLogger(__name__)
    logger = Logger.current_logger()
    logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.DEBUG)
    resume_file =  "data/raw/Soumen Ghosh.pdf"
    app = App(resume_file, python_logger, logger)
    # Process the resume and generate summary
    app.process_resume()

