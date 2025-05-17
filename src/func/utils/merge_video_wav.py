import subprocess
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def merge_video_audio(video_path, audio_path, output_path):
    cmd = [
        "ffmpeg",
        "-i",
        video_path,
        "-i",
        audio_path,
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-shortest",
        output_path,
    ]

    subprocess.run(cmd, check=True)


# Gọi hàm
merge_video_audio(
    "../tmp/video_only.mp4", 
    "../tmp/mixed_snr5.wav", 
    "../tmp/video_with_noisy.mp4"
)

