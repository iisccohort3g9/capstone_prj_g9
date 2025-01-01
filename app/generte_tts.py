import os
from pydub import AudioSegment
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from io import BytesIO

class GenerateTTS:

    def __init__(self, logging):
        self.logging = logging
        self.elevenlabs_api_key = os.getenv("ELEVEN_LABS_API_KEY")
        self.client = ElevenLabs(
            api_key=self.elevenlabs_api_key,
        )

    def text_to_speech_in_memory(self,text: str) -> BytesIO:
        """
        Convert text to speech and store the audio in-memory as an MP3.

        Args:
            text (str): The text to be converted to speech.

        Returns:
            BytesIO: A BytesIO object containing the MP3 audio data.
        """
        # Calling the text_to_speech conversion API
        response = self.client.text_to_speech.convert(
            voice_id="21m00Tcm4TlvDq8ikWAM",  # Adam pre-made voice
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_turbo_v2_5",
            voice_settings=VoiceSettings(
                stability=0.0,
                similarity_boost=1.0,
                style=0.0,
                use_speaker_boost=True,
            ),
        )

        # Combine chunks of the response into a single BytesIO object
        audio_stream = BytesIO()
        for chunk in response:
            if chunk:
                audio_stream.write(chunk)

        # Seek to the beginning of the stream for further processing
        audio_stream.seek(0)
        self.logging.info("MP3 audio is now available in-memory.")
        return audio_stream

    def convert_mp3_to_wav_in_memory(self,mp3_stream: BytesIO) -> BytesIO:
        """
        Convert an in-memory MP3 stream to an in-memory WAV stream.

        Args:
            mp3_stream (BytesIO): A BytesIO object containing MP3 audio data.

        Returns:
            BytesIO: A BytesIO object containing the WAV audio data.
        """
        # Load the MP3 audio from the BytesIO stream
        audio = AudioSegment.from_file(mp3_stream, format="mp3")

        # Convert to WAV and store in a new BytesIO object
        wav_stream = BytesIO()
        audio.export(wav_stream, format="wav")
        wav_stream.seek(0)
        self.logging.info("MP3 audio has been converted to WAV format in-memory.")
        return wav_stream
