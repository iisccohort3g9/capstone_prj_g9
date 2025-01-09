import io
import tempfile
import gradio as gr
import requests


# Function to get the video content from the FastAPI endpoint
def text_to_video(file, jd_text):
    # Send POST request to FastAPI
    # body = {"resume_text": input_text}
    with open(file.name, "rb") as f:
        files = {"file": (file.name, f, "application/pdf")}

        response = requests.post("http://localhost:8000/generate-video", data=jd_text, files=files)

    if response.status_code == 200:
        # Get the video content from the response (which is in the form of a stream)
        response_json = response.json();
        video_stream = io.BytesIO(response_json["stream"])
        jd_similarity = response_json["jd_similarity"]
        resume_summary = response_json["summary_text"]

        # Create a temporary file to save the video
        temp_video_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
        temp_video_path = temp_video_file.name

        # Write the video stream to the temporary file
        with open(temp_video_path, 'wb') as video_file:
            video_file.write(video_stream.read())

            if int(jd_similarity) < 0.5:
                fit = "NOT GOOD FIT"
            elif int(jd_similarity) >= 0.5 and int(jd_similarity) < 0.7:
                fit = "GOOD FIT"
            else:
                fit = "PERFECT MATCH"

        # Return the path to the temporary video file
        return temp_video_path,fit,resume_summary
    else:
        return "Error: Video generation failed"


# Gradio interface
with gr.Blocks() as app:
    gr.Markdown("### HR Resume Summary Video Generator")

    with gr.Row():
        # text_input = gr.TextArea(label="Enter Resume Text", placeholder="Type your resume or text here...")
        pdf_input = gr.File(label="Upload PDF", file_count="single")
        jd_text_input = gr.Textbox(label="Jd summary", placeholder="Enter the Job description...")
        video_output = gr.Video(label="Generated Video")

    submit_button = gr.Button("Generate Video")
    resume_summary_area_output = gr.Textbox(label="Resume Summary", lines=20, placeholder="Generated Resume summary...", interactive=False)
    jd_similarity_output = gr.Textbox(label="Jd similarity", placeholder="Candidate JD Match", interactive=False)
    submit_button.click(text_to_video, inputs=[pdf_input, jd_text_input], outputs=[video_output,jd_similarity_output,resume_summary_area_output])

# Launch the app
app.launch()