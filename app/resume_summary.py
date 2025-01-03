import os
from clearml import Task, Logger
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate
)


class ResumeSummary:

    def __init__(self, resume_data, logger, callbacks=None):
        self.logger = logger
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.llm_name = "gpt-4o-mini"
        self.resume_data = resume_data
        self.callbacks = callbacks if callbacks else []

    def get_prompt(self):
        # Generate a Json Output from the LLM using Prompt Engg & LLM
        return ChatPromptTemplate.from_messages([("system",'''You are an AI bot designed to act as a professional for parsing resumes. You are given with resume and your job is to extract the following information from the resume:
                              1. full name
                              2. email id
                              3. github portfolio
                              4. linkedIn id
                              5. employment details (latest 2)
                              6. technical skills (top 5)
                              7. soft skills (top 5)
                              Give the extracted information strictly in json format only. Don't hallucinate while parsing, if the required information isn't present, say that its "not available" ''' ),
                                          ("human",'''Here's the candidate profile mentioned- {input}''')])

    def generate_resume_summary(self):
        llm = ChatOpenAI(model_name=self.llm_name, temperature=0, api_key=self.openai_api_key, callbacks = self.callbacks)
        # Trigger the callbacks, if provided
        for callback in self.callbacks:
            callback.on_start(self)
        # create chain
        chain2 = self.get_prompt() | llm | StrOutputParser()
        result = chain2.invoke({'input': self.resume_data})
        self.logger.report_text(f"chain2 result {result}")

        # Generate a 150 word summary using the result
        prompt_json_summary = ChatPromptTemplate.from_messages(
                 [("system", '''You are an HR recruitment assistant designed to create candidate profile summaries. You are given a Json input with candidate details and your job is to create a summary out of it strictly upto 150 words.
                   Don't hallucinate while creating summaries, if the required information isn't present, say that its "not available" '''),
                   ("human", '''Here's the candidate json profile mentioned- {json_input}''')])

        chain3 = prompt_json_summary | llm | StrOutputParser()
        result_summary = chain3.invoke({'json_input': result})
        self.logger.report_text(f"chain3 result {result_summary}")
        callbacks.flush_tracker(langchain_asset=llm, name="summary generation")
        # If callback handler exists, report progress or log to ClearML
        for callback in self.callbacks:
            callback.on_end(self)

        return result_summary




