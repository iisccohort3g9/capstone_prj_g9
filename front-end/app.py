import io
import tempfile
import gradio as gr
import requests

# Function to get the video content from the FastAPI endpoint
def text_to_video(file):
    # Send POST request to FastAPI
    # body = {"resume_text": input_text}
    with open(file.name, "rb") as f:
        files = {"file": (file.name, f, "application/pdf")}
        response = requests.post("http://localhost:8000/generate-video", files=files)

    if response.status_code == 200:
        # Get the video content from the response (which is in the form of a stream)
        video_stream = io.BytesIO(response.content)
        
        # Create a temporary file to save the video
        temp_video_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
        temp_video_path = temp_video_file.name
        
        # Write the video stream to the temporary file
        with open(temp_video_path, 'wb') as video_file:
            video_file.write(video_stream.read())
        
        # Return the path to the temporary video file
        return temp_video_path
    else:
        return "Error: Video generation failed"

# Gradio interface
with gr.Blocks() as app:
    gr.Markdown("### HR Resume Summary Video Generator")

    with gr.Row():
        # text_input = gr.TextArea(label="Enter Resume Text", placeholder="Type your resume or text here...")
        pdf_input = gr.File(label="Upload PDF", file_count="single")
        video_output = gr.Video(label="Generated Video")

    submit_button = gr.Button("Generate Video")
    submit_button.click(text_to_video, inputs=pdf_input, outputs=video_output)

# Launch the app
app.launch()
