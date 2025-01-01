import pandas as pd
import re
import os


def clean_text(text):
    """Remove special characters, multiple spaces, and newlines."""
    text = re.sub(r'\n+', ' ', text)  # Remove newlines
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single space
    text = re.sub(r'[^a-zA-Z0-9., ]', '', text)  # Remove special characters
    return text.strip()


def preprocess_resumes(input_csv, output_csv):
    """Preprocess resumes from CSV file."""
    if not os.path.exists(input_csv):
        raise FileNotFoundError("Input file not found!")

    # Load dataset
    df = pd.read_csv(input_csv)

    # Clean 'Resume' column
    if 'Resume' in df.columns:
        df['cleaned_resume'] = df['Resume'].apply(clean_text)
    else:
        raise KeyError("'Resume' column not found in dataset")

    # Save cleaned data
    df.to_csv(output_csv, index=False)
    print(f"Preprocessed resumes saved to {output_csv}")


if __name__ == "__main__":
    input_file = "../../data/raw/resume-dataset.csv"
    output_file = "../../data/processed/resumes_cleaned.csv"
    preprocess_resumes(input_file, output_file)
