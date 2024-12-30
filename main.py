import tempfile
import gradio as gr
from gtts import gTTS
from src.summarize import generate_summary
from moviepy.editor import *
import os

# Dummy function to return a video file based on input text
def text_to_video(input_text):
    # Map the input text to a video file (replace with your logic)
    # video_file = "result_voice.mp4"  # Path to the video file
    summary_text = generate_summary(input_text)
    print(summary_text)
    """Generate video with TTS audio and background image for Gradio."""
    # Generate TTS audio in memory
    tts = gTTS(summary_text)
    audio_buffer = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    tts.write_to_fp(audio_buffer)
    audio_buffer.flush()
    audio_buffer.close()  # Close to ensure data is written

    # Load audio from the temporary file
    audio = AudioFileClip(audio_buffer.name)
    background_image = "./data/background.jpg"
    # Set up background
    if background_image:
        clip = ImageClip(background_image).set_duration(audio.duration)
    else:
        clip = ColorClip(size=(1280, 720), color=(255, 255, 255), duration=audio.duration)

    # Combine video and audio
    video = clip.set_audio(audio)

    # Write video to a temporary file
    temp_video_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    temp_video_path = temp_video_file.name
    video.write_videofile(temp_video_path, fps=24, codec="libx264", audio_codec="aac")
    
    # Clean up temporary audio file
    audio.close()
    video.close()

    return temp_video_path

# Gradio interface
with gr.Blocks() as app:
    gr.Markdown("HR Resume Summary")
    
    with gr.Row():
        text_input = gr.TextArea(label="Enter Text", placeholder="Type something...")
        video_output = gr.Video(label="Output Video")

    submit_button = gr.Button("Submit")
    submit_button.click(text_to_video, inputs=text_input, outputs=video_output)

# Launch the app
app.launch()
