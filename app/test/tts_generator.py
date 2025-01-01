from gtts import gTTS
import pandas as pd
import os
from clearml import Task

# Use the ClearML SDK to initialize and define the task for audio generation
task = Task.init(
    project_name="Resume Summary AV Generation",
    task_name="Generate Audio",
    task_type=Task.TaskTypes.data_processing
)

# Log the parameters
parameters = {
    "input_csv": "data/processed/resumes_with_summary.csv",
    "audio_dir": "output/summary_audio/",
    "audio_format": "mp3",
    "tts_engine": "Google TTS"
}

task.connect(parameters)

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
        # Check if the file exists
        if os.path.exists(audio_path):
            print(f"Audio file already exists for row {idx}: {audio_path}. Skipping...")
            continue
        
        # Generate audio if it does not exist
        generate_audio(row['summary'], audio_path)
        print(f"Generated audio: {audio_path}")
    
    # Track the generated audio files as artifacts    
    audio_files = [os.path.join(output_dir, f"summary_{idx}.mp3") for idx in range(len(df))]
    
    
    for audio_path in audio_files:
        artifact_name = f"Audio File: {os.path.basename(audio_path)}"
        
        # Check if the artifact already exists
        # if artifact_name in existing_artifacts:
        #     print(f"Artifact {artifact_name} already exists. Skipping upload...")
        #     continue
        
        # Upload the artifact if it does not exist
        if os.path.exists(audio_path):  # Ensure the file exists locally
            task.upload_artifact(artifact_name, audio_path)
            print(f"Uploaded artifact: {artifact_name}")
        else:
            print(f"File {audio_path} does not exist locally. Skipping...")



if __name__ == "__main__":
    input_file = "data/processed/resumes_with_summary.csv"
    output_directory = "output/summary_audio/"
    process_summaries(input_file, output_directory)
