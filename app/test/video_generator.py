from moviepy.editor import TextClip, CompositeVideoClip, ColorClip, AudioFileClip, ImageClip
from moviepy.config import change_settings
import os

change_settings({"IMAGEMAGICK_BINARY": None})  # Disable ImageMagick


def generate_video(audio_path, output_path, summary_path, background_image=None):
    """Generate video with audio and background image."""
    if background_image:
        clip = ImageClip(background_image).set_duration(AudioFileClip(audio_path).duration)
    else:
        clip = ColorClip(size=(1280, 720), color=(255, 255, 255), duration=AudioFileClip(audio_path).duration)
        
    # 2. Create a Text Clip (Overlay)
    # Specify the full path to the Arial font file
    font_path = "arial.ttf"  # Full path to Arial font
   
    if not os.path.exists(font_path):
        print(f"Font file not found at {font_path}")
    else:
        print(f"Font file found at {font_path}")
    
    text_clip = TextClip(
        summary_path, 
        fontsize=50, 
        color='white', 
        font=font_path,  # Install the font if unavailable
        size=(1600, None),  # Text box size
        method='caption'  # Wrap text automatically
    )
    
    # 3. Add Background Audio (TTS Audio File)
    audio = AudioFileClip(audio_path)
    
    # Combine Video and Text
    final_clip = CompositeVideoClip([clip, text_clip.set_position("center")])
    final_clip = final_clip.set_audio(audio)
    
    final_clip.write_videofile(output_path, fps=24, codec='libx264')
    print(f"Generated video: {output_path}")


if __name__ == "__main__":
    audio_dir = "output/summary_audio/"
    video_dir = "output/videos/"
    summary_dir = "output/summary_texts"
    background_image = "data/background.jpg"  # Optional
    # Path to the Windows Fonts directory
    # font_dir = "C:/Windows/Fonts"

    # List all .ttf and .otf files in the font directory
    # font_files = [f for f in os.listdir(font_dir) if f.endswith(('.ttf', '.otf'))]
    # print(font_files)

    os.makedirs(video_dir, exist_ok=True)

    for audio_file in os.listdir(audio_dir):
        if audio_file.endswith(".mp3"):
            audio_path = os.path.join(audio_dir, audio_file)
            video_path = os.path.join(video_dir, audio_file.replace(".mp3", ".mp4"))
            # Derive the corresponding summary text file path
            summary_filename = audio_file.replace(".mp3", ".txt") 
            summary_path = os.path.join(summary_dir, summary_filename)
            # Check if the summary text file exists
            if os.path.exists(summary_path):
                generate_video(audio_path, video_path, summary_path, background_image)
            else:
                print(f"Warning: Summary file not found for {audio_file} at {summary_path}")

                
