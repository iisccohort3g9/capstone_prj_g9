# src/video_gen.py
import requests

def generate_video(script, audio_file, output_file):
    api_url = "https://api.sora.ai/generate"
    response = requests.post(api_url, json={"script": script, "audio_file": audio_file})
    with open(output_file, "wb") as f:
        f.write(response.content)
