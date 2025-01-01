import openai
import pandas as pd
import os

# Set your OpenAI API key here
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_summary(resume_text):
    """
    Generate a professional summary for a resume using OpenAI's new API format.
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are an assistant that generates concise professional summaries for resumes."},
                {"role": "user", "content": f"Summarize this resume into a concise professional summary:\n{resume_text}"}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating summary: {e}")
        return ""
def summarize_resumes(input_csv, output_csv):
    """
    Reads resumes from a CSV file, generates summaries, and saves the results to another CSV file.
    """
    df = pd.read_csv(input_csv)
    if 'cleaned_resume' not in df.columns:
        raise ValueError("Input CSV must have a 'cleaned_resume' column")

    # Apply the summary generation function to each resume
    print("Generating summaries...")
    df['summary'] = df['cleaned_resume'].apply(generate_summary)

    # Save the summarized data to a new CSV file
    df.to_csv(output_csv, index=False)
    print(f"Summaries saved to {output_csv}")

if __name__ == "__main__":
    input_csv = "../data/processed/resumes_cleaned.csv"  # Input preprocessed resumes
    output_csv = "../data/processed/resumes_with_summary.csv"  # Output with summaries
    summarize_resumes(input_csv, output_csv)
