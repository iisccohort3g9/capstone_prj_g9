import io
import tempfile
import gradio as gr
import requests


# Function to get the video content from the FastAPI endpoint
def text_to_video(file, jd_text):
    # Send POST request to FastAPI
    with open(file.name, "rb") as f:
        files = {"file": (file.name, f, "application/pdf")}
        data = {"job_description": jd_text}
        response = requests.post("http://localhost:8000/generate-video", files=files, data=data)

    if response.status_code == 200:
        # Get the video content from the response (jd_similarity, summary_text, and video URL)
        response_json = response.json()
        video_url = response_json["video_url"]
        jd_similarity = response_json["jd_similarity"]
        resume_summary = response_json["summary_text"]

        # Determine the fit category based on jd_similarity
        if jd_similarity < 0.5:
            fit = "NOT GOOD FIT"
        elif 0.5 <= jd_similarity < 0.7:
            fit = "GOOD FIT"
        else:
            fit = "PERFECT MATCH"
    response = requests.get(f"http://localhost:8000/video/{video_url}")
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
        return temp_video_path, fit, resume_summary
    else:
        return "Error: Video generation failed"


# Gradio interface
with gr.Blocks() as app:
    gr.Markdown("### HR Resume Summary Video Generator")

    with gr.Row():
        pdf_input = gr.File(label="Upload PDF", file_count="single")
        jd_text_input = gr.Textbox(label="Job Description", placeholder="Enter the Job description...")

    submit_button = gr.Button("Evaluate and Generate")
    with gr.Row():
        video_output = gr.Video(label="Generated Video")
        resume_summary_area_output = gr.Textbox(label="Resume Summary", lines=20, placeholder="Generated Resume summary...", interactive=False)
    jd_similarity_output = gr.Textbox(label="Job Description Similarity", placeholder="Candidate JD Match", interactive=False)

    # Update the button click to use the updated text_to_video function
    submit_button.click(text_to_video, inputs=[pdf_input, jd_text_input], outputs=[video_output, jd_similarity_output, resume_summary_area_output])

# Launch the app
app.launch()