from gtts import gTTS
import pandas as pd
import os
import imageio
import numpy as np  # Import numpy for array manipulation
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, AudioFileClip
from rouge_score import rouge_scorer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import whisper


def generate_audio(summary_text, output_path):
    """Convert text to speech and save as audio file."""
    tts = gTTS(summary_text)
    tts.save(output_path)

def generate_segments():
    model = whisper.load_model("small")
    result = model.transcribe("output\summary_audio\summary_1.mp3")
    print(result["text"])


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
        
        # Check if the video file already exists
        if os.path.exists(output_video):
            print(f"Video already exists for row {idx}: {output_video}. Skipping...")
            continue  # Skip to the next row
        
        # Check if the audio file exists before proceeding
        if not os.path.exists(audio_file):
            print(f"Audio file missing for row {idx}: {audio_file}")
            continue
        
        # Save the current summary to a text file for FFmpeg
        with open(text_file, "w") as f:
            f.write(row['summary'])
            
        # Use ImageIO to generate the video
        print(f"Generating Video for row {idx}...")
        
        # Create a writer object with the necessary parameters
        writer = imageio.get_writer(output_video, fps=24)
        

        # Create a blank frame (or use an image as the background)
        height, width = 1080, 1920
        background_color = [0, 0, 255]  # Blue in RGB
        frame = imageio.core.util.Array(np.full((height, width, 3), background_color, dtype=np.uint8))

        # Add the text overlay
        text = row['summary']  # Assuming 'row' is already defined with the summary text

        # Font setup
        font_path = "arial.ttf"  # Replace with the correct path to your font
        font_size = 50  # Start with a font size (you can adjust this)
        font = ImageFont.truetype(font_path, size=font_size)

        # Define a function for wrapping text within the given width
        def wrap_text(text, font, max_width):
            lines = []
            words = text.split(' ')
            current_line = ""

            for word in words:
                test_line = current_line + " " + word if current_line else word
                bbox = draw.textbbox((0, 0), test_line, font=font)
                text_width, _ = bbox[2] - bbox[0], bbox[3] - bbox[1]

                if text_width <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word

            if current_line:
                lines.append(current_line)

            return lines

        # Create the frame and add text
        img = Image.fromarray(frame)
        draw = ImageDraw.Draw(img)

        # Wrap the text and get the lines
        max_width = width - 40  # Max width for the text box (leave some padding)
        text_lines = wrap_text(text, font, max_width)

        # Calculate the height of the wrapped text
        total_text_height = sum([draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in text_lines])

        # Calculate starting position to center the text vertically and horizontally
        y_position = (height - total_text_height) // 2
        x_position = (width - max_width) // 2

        # Draw each line of the wrapped text
        for line in text_lines:
            draw.text((x_position, y_position), line, font=font, fill="white")
            y_position += draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1]  # Move the y position for the next line

        # Convert the image back to a NumPy array
        frame_with_text = np.array(img)

        # Append the frame to the video (repeat this if you want the text to stay longer)
        for _ in range(240):  # Display the text for 10 seconds at 24 fps
            writer.append_data(frame_with_text)

        # Add the audio to the video
        writer.close()

        # Create a VideoFileClip object (using moviepy)
        video_clip = VideoFileClip(output_video)

        # Create an AudioFileClip object (using moviepy)
        audio_clip = AudioFileClip(audio_file)
        audio_clip = audio_clip.volumex(1.0)

        # Set the audio for the video and write the final output
        final_video = video_clip.set_audio(audio_clip)

        # Write the final video with the audio
        final_video.write_videofile(output_video, codec="libx264", audio_codec="libmp3lame", audio_bitrate="192k")

        print(f"Video Generated: {output_video}")
        
    def read_text_file(file_path):
        """Read and return the content of a text file."""
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return ""
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
        
    # Function to calculate ROUGE-1 scores
    def calculate_rouge_1(reference, summary):
        scorer = rouge_scorer.RougeScorer(['rouge1'], use_stemmer=True)
        scores = scorer.score(reference, summary)
        return scores['rouge1']

    # Function to calculate Cosine Similarity
    def calculate_cosine_similarity(reference, summary):
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([reference, summary])
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return cosine_sim[0][0]
        
    generated_summary_path = "summary_text_0.txt"
    reference_text_path = "reference_job_text.txt"
    
    # Compute ROUGE-L scores
    reference_summary = read_text_file(reference_text_path)
    generated_summary = read_text_file(generated_summary_path)
    
    # Debugging: Ensure summaries are correctly read
    # print(f"Reference Summary for row {idx}: {reference_summary}")
    # print(f"Generated Summary for row {idx}: {generated_summary}")
    
 
    # Compute ROUGE-1
    rouge1_scores = calculate_rouge_1(reference_summary, generated_summary)
    print(f"ROUGE-1 Scores: Precision: {rouge1_scores.precision:.4f}, Recall: {rouge1_scores.recall:.4f}, F1-Score: {rouge1_scores.fmeasure:.4f}")
    
    # Compute Cosine Similarity
    cosine_sim = calculate_cosine_similarity(reference_summary, generated_summary)
    print(f"Cosine Similarity: {cosine_sim:.4f}")
    
    # Use Rouge-1 or similarity score, cosine similarity

        
    
if __name__ == "__main__":
    input_file = "data/processed/resumes_with_summary.csv"
    output_directory = "output/summary_audio"
    process_summaries(input_file, output_directory)
    # create_video()
