# src/tts.py
from gtts import gTTS

def generate_audio(script, output_file):
    tts = gTTS(script, lang="en")
    tts.save(output_file)
