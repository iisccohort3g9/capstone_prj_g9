# src/preprocess.py
import textract
import os
import json

def extract_resume_sections(text):
    """Dummy function to split resume text into structured sections."""
    sections = {
        "summary": text[:300],
        "skills": text[300:600],
        "experience": text[600:900],
        "education": text[900:1200]
    }
    return sections

def preprocess_resumes(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf") or filename.endswith(".docx"):
            text = textract.process(os.path.join(input_dir, filename)).decode("utf-8")
            structured_data = extract_resume_sections(text)
            with open(os.path.join(output_dir, f"{filename}.json"), 'w') as f:
                json.dump(structured_data, f)

if __name__ == "__main__":
    preprocess_resumes("data/raw_resumes", "data/processed_resumes")
