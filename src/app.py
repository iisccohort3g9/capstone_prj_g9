# src/app.py
import gradio as gr
from summarizer import generate_script
from tts import generate_audio
from video_gen import generate_video

def process_resume(file):
    # Generate script
    script = generate_script(file.name, "models/fine-tuned-gpt")

    # Convert to audio
    audio_file = "data/outputs/audio.mp3"
    generate_audio(script, audio_file)

    # Generate video
    video_file = "data/outputs/video.mp4"
    generate_video(script, audio_file, video_file)

    return script, audio_file, video_file

app = gr.Interface(
    fn=process_resume,
    inputs=gr.inputs.File(label="Upload Resume"),
    outputs=[
        gr.outputs.Textbox(label="Generated Script"),
        gr.outputs.Audio(label="Audio Output"),
        gr.outputs.File(label="Video Output")
    ]
)

if __name__ == "__main__":
    app.launch()
