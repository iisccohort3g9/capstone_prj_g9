import os
import time
import numpy as np
from clearml import Task, Logger
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate
)
from langchain_openai import OpenAIEmbeddings

class CVSimilarity:

    def __init__(self, resume_summary, logger, jd_text):
        self.logger = logger
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.llm_name = "gpt-4o-mini"
        self.resume_summary = resume_summary
        self.jd_text = jd_text
        self.embedding = OpenAIEmbeddings(model='text-embedding-3-small', api_key=self.openai_api_key)

    def cosine_similarity(self,vector1, vector2):
        # Ensure that the vectors are numpy arrays
        vector1 = np.array(vector1)
        vector2 = np.array(vector2)

        # Calculate the dot product of the vectors
        dot_product = np.dot(vector1, vector2)

        # Calculate the magnitude (norm) of the vectors
        norm_vector1 = np.linalg.norm(vector1)
        norm_vector2 = np.linalg.norm(vector2)

        # Compute cosine similarity
        if norm_vector1 == 0 or norm_vector2 == 0:
            return 0  # Avoid division by zero
        return dot_product / (norm_vector1 * norm_vector2)

    def calculate_similarity(self):
        llm = ChatOpenAI(model_name=self.llm_name, temperature=0, api_key=self.openai_api_key)

        prompt_jd_summary = ChatPromptTemplate.from_messages([("system", '''You are an HR recruitment assistant designed to create Job description summaries. You are given a job description for a specific role and your job is to create a summary focusing on the responsibilities & requirements of the given role out of it strictly upto 150 words.
        Ensure that you focus on both the technical & the non technical requirements both & don't hallucinate while creating summaries. If any type of requirement isn't present, ignore that but don't hallucinate'''),
                                                              ("human",
                                                               '''Here's the Job description mentioned- {jd_input}''')])
        chain4 = prompt_jd_summary | llm | StrOutputParser()
        jd_summary = chain4.invoke({'jd_input': self.jd_text})
        self.logger.report_text(f"jd summary {jd_summary}")

        jd_embedding = self.embedding.embed_query(jd_summary)
        cv_summary_embedding = self.embedding.embed_query(self.resume_summary)

        cv_similarity = self.cosine_similarity(cv_summary_embedding, jd_embedding)
        self.logger.report_text(f"cv similarity {cv_similarity}")
        return cv_similarity


