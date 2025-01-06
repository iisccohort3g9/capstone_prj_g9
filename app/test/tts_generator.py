from gtts import gTTS
import pandas as pd
import ffmpeg
import os
from clearml import Task

task = Task.init(
    project_name="Summary AV Generation",
    task_name="Generate Audio",
    task_type=Task.TaskTypes.processing
)

task.connect({
    "input_csv": "data/processed/resumes_with_summary.csv",
    "audio_dir": "output\summary_audio",
    "audio_format": "mp3",
    "tts_engine": "Google TTS"
})


def generate_audio(summary_text, output_path):
    """Convert text to speech and save as audio file."""
    tts = gTTS(summary_text)
    tts.save(output_path)


def process_summaries(input_csv, output_dir):
    """Generate audio for all summaries."""
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(input_csv)
    audio_dir = "output/summary_audio"
    video_output_dir = "output/videos"

    # for idx, row in df.iterrows():
    for idx, row in df.head(2).iterrows():  # Just iterate over 2 rows of summary for checking the logic, will remove later and uncomment above line
        audio_path = os.path.join(output_dir, f"summary_{idx}.mp3")
        # Check if the audio file already exists
        if os.path.exists(audio_path):
            print(f"Audio already exists: {audio_path}")
            continue  # Skip generation
        generate_audio(row['summary'], audio_path)
        print(f"Generated audio: {audio_path}")
    
    # # Iterate over the first 2 rows of the DataFrame
    for idx, row in df.head(2).iterrows():
        # Define dynamic paths for audio, text file, and output video
        audio_file = os.path.join(audio_dir, f"summary_{idx}.mp3")
        text_file = f"summary_text_{idx}.txt"
        output_video = os.path.join(video_output_dir, f"summary_video_{idx}.mp4")
        
        # Check if the audio file exists before proceeding
        if not os.path.exists(audio_file):
            print(f"Audio file missing for row {idx}: {audio_file}")
            continue
        
        # Save the current summary to a text file for FFmpeg
        with open(text_file, "w") as f:
            f.write(row['summary'])
        
        # FFmpeg Command
        ffmpeg_command = f"""
        ffmpeg -f lavfi -i color=c=blue:s=1920x1080:d=10 \\
            -vf "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf: \\
            textfile={text_file}:fontcolor=white:fontsize=36:x=(w-text_w)/2:y=(h-text_h)/2" \\
            -i "{audio_file}" -c:v libx264 -c:a aac -strict experimental \\
            -shortest "{output_video}"
        """
        
        # Run the FFmpeg Command
        print(f"Generating Video for row {idx}...")
        os.system(ffmpeg_command)
        print(f"Video Generated: {output_video}")
        
    


if __name__ == "__main__":
    input_file = "data/processed/resumes_with_summary.csv"
    output_directory = "output/summary_audio"
    process_summaries(input_file, output_directory)
    # create_video()
