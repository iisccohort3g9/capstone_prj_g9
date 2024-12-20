from moviepy.editor import *
import os


def generate_video(audio_path, output_path, background_image=None):
    """Generate video with audio and background image."""
    if background_image:
        clip = ImageClip(background_image).set_duration(AudioFileClip(audio_path).duration)
    else:
        clip = ColorClip(size=(1280, 720), color=(255, 255, 255), duration=AudioFileClip(audio_path).duration)

    audio = AudioFileClip(audio_path)
    video = clip.set_audio(audio)
    video.write_videofile(output_path, fps=24)
    print(f"Generated video: {output_path}")


if __name__ == "__main__":
    audio_dir = "../output/summary_audio/"
    video_dir = "../output/videos/"
    background_image = "../data/background.jpg"  # Optional

    os.makedirs(video_dir, exist_ok=True)

    for audio_file in os.listdir(audio_dir):
        if audio_file.endswith(".mp3"):
            audio_path = os.path.join(audio_dir, audio_file)
            video_path = os.path.join(video_dir, audio_file.replace(".mp3", ".mp4"))
            generate_video(audio_path, video_path, background_image)
