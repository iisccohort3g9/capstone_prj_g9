import os
from pathlib import Path
import tempfile
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import io
from fastapi.responses import StreamingResponse
from clearml import Task, Logger
from langchain_community.callbacks import ClearMLCallbackHandler
from langchain_core.callbacks import StdOutCallbackHandler
from generte_tts import GenerateTTS
from resume_file_reader import ResumeFileReader
from resume_summary import ResumeSummary
import subprocess
from pydub import AudioSegment

# Initialize ClearML Task
# task = Task.init(
#     project_name="Resume Summary AV Generation",
#     task_name="Generate Resume Summary",
#     task_type=Task.TaskTypes.data_processing
# )
# # Initialize ClearML Logger
logger = Logger.current_logger()
# Set up ClearML Callback Handler
# callback_handler = ClearMLCallbackHandler(
#     task_type="inference",
#     project_name="Resume Summary AV Generation",
#     task_name="Generate Resume Summary",
#     tags=["test"],
#     # Change the following parameters based on the amount of detail you want tracked
#     visualize=True,
#     complexity_metrics=False,
#     stream_logs=True
# )
# callbacks = (StdOutCallbackHandler(), callback_handler)

app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def is_valid_file(file: UploadFile) -> bool:
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in ['.docx', '.pdf']:
        return False
    return True


@app.post('/generate-video')
async def generate_video(file: UploadFile = File(...)):
    # Check if the file is .docx or .pdf
    if not is_valid_file(file):
        raise HTTPException(status_code=400, detail="File must be a .docx or .pdf")

    # Connect parameters to task
    # parameters = {"resume_file": file}
    # task.connect(parameters)
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
        # Save the file content to the temp file
        content = await file.read()  # Read the content of the file
        temp_file.write(content)  # Save it to the temp file

        temp_file_path = temp_file.name  # Get the file path for further processing
        print(f"Temporary file saved at {temp_file_path}")

    rfr = ResumeFileReader(temp_file_path)
    resume_data = rfr.extract_text_from_file()
    print(resume_data)
    # rfs = ResumeSummary(resume_data, logger)
    # summary_text = rfs.generate_resume_summary()
    summary_text = """Highly skilled AI Engineer with a strong foundation in machine learning, deep learning, and natural language processing. Over 5 years of experience designing, developing, and deploying AI models for various applications, including computer vision, speech recognition, and predictive analytics. Proficient in Python, TensorFlow, PyTorch, and other AI/ML frameworks, with hands-on expertise in building scalable solutions and optimizing model performance. Strong understanding of algorithms, data structures, and big data technologies, with a focus on creating efficient, production-ready systems. Experienced in working with cloud platforms like AWS, Google Cloud, and Azure for deploying AI models at scale. Passionate about leveraging cutting-edge AI technologies to solve complex problems, drive business innovation, and enhance user experiences. Excellent communication and collaboration skills, with a proven track record of working in agile teams to deliver impactful AI-driven solutions on time."""
    print("Generating summary:", summary_text)
    # Generate TTS audio in memory
    tts = GenerateTTS(logger)
    audio = tts.text_to_speech_in_memory(summary_text)
    # Convert the MP3 data to WAV
    audio_segment = AudioSegment.from_mp3(audio)
    # Create a temporary file to save the audio data
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        audio_segment.export(temp_file.name, format="wav")

    # Get the temporary file's name (path)
    audio_file_path = temp_file.name

    command = ["python", "Wav2Lip/inference.py", "--checkpoint_path", "Wav2Lip/checkpoints/wav2lip_gan.pth", "--face",
               "input_video.mp4", "--audio", audio_file_path]
    print(command)
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    print(result.stdout)
    print(result.stderr)
    for line in result.stdout.splitlines():
        if "Output video file saved to" in line:
            output_file_path = line.split(":")[-1].strip()
            print(f"Video file saved to: {output_file_path}")
    # Read the video file into binary
    with open(output_file_path, "rb") as video_file:
        video_content = video_file.read()

    # Ensure temporary files are cleaned up
    os.remove(temp_file_path)
    os.remove(audio_file_path)
    os.remove(output_file_path)

    # Return video content as streaming response using io.BytesIO
    video_stream = io.BytesIO(video_content)
    video_stream.seek(0)  # Ensure the pointer is at the start of the file
    return StreamingResponse(video_stream, media_type="video/mp4")


if __name__ == "__main__":
    uvicorn.run("api:app", reload=True)