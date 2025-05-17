import subprocess
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def split_video_audio(input_file, video_out, audio_out):
    """
    Tách video (không audio) và âm thanh (WAV, mono, 16kHz) từ một file video đầu vào.

    Parameters:
        input_file (str): Đường dẫn đến file video gốc.
        video_out (str): Đường dẫn file output video không có âm thanh.
        audio_out (str): Đường dẫn file output âm thanh WAV.
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Không tìm thấy file: {input_file}")

    # Tạo thư mục output nếu chưa có
    os.makedirs(os.path.dirname(video_out), exist_ok=True)
    os.makedirs(os.path.dirname(audio_out), exist_ok=True)

    # Tách video không có âm thanh
    cmd_video = [
        "ffmpeg", "-i", input_file,
        "-an",  # disable audio
        "-c:v", "copy",  # copy video stream
        video_out
    ]

    # Tách audio sang WAV (mono, 16kHz)
    cmd_audio = [
        "ffmpeg", "-i", input_file,
        "-vn",               # disable video
        "-acodec", "pcm_s16le",  # WAV format (Linear PCM 16-bit)
        "-ar", "16000",          # sample rate 16kHz
        "-ac", "1",              # mono
        audio_out
    ]

    result_video = subprocess.run(cmd_video, capture_output=True, text=True)
    if result_video.returncode != 0:
        print("Lỗi khi tách video:", result_video.stderr)

    result_audio = subprocess.run(cmd_audio, capture_output=True, text=True)
    if result_audio.returncode != 0:
        print("Lỗi khi tách audio:", result_audio.stderr)




input_path = 'F:\\Ticktok videos\\CutItInHalf.mp4'
video_output = 'D:\\Downloads\\video_only.mp4'
audio_output = 'D:\\Downloads\\audio_only.wav'

split_video_audio(input_path, video_output, audio_output)

