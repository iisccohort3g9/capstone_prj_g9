import os
import re
import json
import pandas as pd


def extract_sections_from_resume(resume_text):
    """
    Extract key sections like Education, Skills, and Experience from resume text.
    Modify regex patterns as needed based on the resume structure.
    """
    sections = {
        "education": None,
        "skills": None,
        "experience": None,
        "summary": None,
    }

    # Extract Education section
    education_pattern = r"(education|academic|qualifications|degree)[\s\S]*?(experience|skills|$)"
    education_match = re.search(education_pattern, resume_text, re.IGNORECASE)
    if education_match:
        sections["education"] = education_match.group().strip()

    # Extract Skills section
    skills_pattern = r"(skills|technologies|proficiencies)[\s\S]*?(experience|education|$)"
    skills_match = re.search(skills_pattern, resume_text, re.IGNORECASE)
    if skills_match:
        sections["skills"] = skills_match.group().strip()

    # Extract Experience section
    experience_pattern = r"(experience|projects|employment history)[\s\S]*?(skills|education|$)"
    experience_match = re.search(experience_pattern, resume_text, re.IGNORECASE)
    if experience_match:
        sections["experience"] = experience_match.group().strip()

    # Extract Summary (First few lines of resume)
    summary_match = resume_text.split("\n")[:3]
    sections["summary"] = " ".join([line.strip() for line in summary_match if line.strip()])

    return sections


def preprocess_csv(input_csv, output_dir):
    """
    Process resumes from a CSV file and save as JSON files in the output directory.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Load the dataset
    data = pd.read_csv(input_csv)

    for index, row in data.iterrows():
        try:
            resume_text = row['Resume']
            category = row['Category']  # Metadata

            # Extract structured data
            structured_data = extract_sections_from_resume(resume_text)
            structured_data["category"] = category  # Add category metadata

            # Save structured data as JSON
            json_filename = f"resume_{index + 1}.json"
            with open(os.path.join(output_dir, json_filename), 'w') as f:
                json.dump(structured_data, f, indent=4)

            print(f"Processed: Resume {index + 1}")
        except Exception as e:
            print(f"Failed to process Resume {index + 1}: {e}")


if __name__ == "__main__":
    input_csv = "../data/raw_resumes/UpdatedResumeDataSet.csv"  # Update with the path to your CSV file
    output_directory = "../data/processed_resumes"
    preprocess_csv(input_csv, output_directory)
