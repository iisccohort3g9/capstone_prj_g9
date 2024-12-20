from gtts import gTTS
import pandas as pd
import os


def generate_audio(summary_text, output_path):
    """Convert text to speech and save as audio file."""
    tts = gTTS(summary_text)
    tts.save(output_path)


def process_summaries(input_csv, output_dir):
    """Generate audio for all summaries."""
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(input_csv)

    for idx, row in df.iterrows():
        audio_path = os.path.join(output_dir, f"summary_{idx}.mp3")
        generate_audio(row['summary'], audio_path)
        print(f"Generated audio: {audio_path}")


if __name__ == "__main__":
    input_file = "../data/processed/resumes_with_summary.csv"
    output_directory = "../output/summary_audio/"
    process_summaries(input_file, output_directory)
