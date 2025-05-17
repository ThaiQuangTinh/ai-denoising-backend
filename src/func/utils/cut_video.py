import subprocess
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


def trim_video(input_path, output_path, start_time="00:00:00", duration="00:00:10"):
    """
    Cắt một đoạn video từ thời gian start_time với độ dài duration.
    """
    cmd = [
        "ffmpeg",
        "-i",
        input_path,
        "-ss",
        start_time,
        "-t",
        duration,
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        "-strict",
        "experimental",
        output_path,
    ]

    subprocess.run(cmd, check=True)

trim_video('../tmp/video_only.mp4', '../tmp/video_only2.mp4', '00:00:00', '00:00:20')