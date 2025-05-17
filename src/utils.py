import os
import subprocess

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Lấy độ dài video bằng ffprobe
def get_duration_of_video(video_path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", video_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return float(result.stdout)

# Hàm tách video và audio
def split_video_audio(input_file, video_out, audio_out):
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Không tìm thấy file: {input_file}")

    os.makedirs(os.path.dirname(video_out), exist_ok=True)
    os.makedirs(os.path.dirname(audio_out), exist_ok=True)

    # Lấy thời lượng video (giây)
    duration = get_duration_of_video(input_file)

    # Tách video không có âm thanh
    cmd_video = [
        "ffmpeg", "-i", input_file,
        "-an",  # disable audio
        "-c:v", "copy",
        video_out
    ]

    # Tách audio WAV (mono, 16kHz) và cắt đúng độ dài video
    cmd_audio = [
        "ffmpeg", "-i", input_file,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        "-af", f"apad=pad_dur={duration}",  # Thêm silence nếu ngắn
        "-t", str(duration),  # Ép đúng thời lượng
        audio_out
    ]

    result_video = subprocess.run(cmd_video, capture_output=True, text=True)
    if result_video.returncode != 0:
        print("Error when split video:", result_video.stderr)

    result_audio = subprocess.run(cmd_audio, capture_output=True, text=True)
    if result_audio.returncode != 0:
        print("Error when split audio:", result_audio.stderr)

# Function to merge video and audio
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