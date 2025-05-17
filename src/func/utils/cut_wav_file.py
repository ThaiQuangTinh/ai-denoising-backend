import subprocess
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def trim_wav_file(input_wav, output_wav, start_time, end_time):
    """
    Cắt đoạn âm thanh từ file WAV gốc từ thời gian start_time đến end_time.

    Parameters:
        input_wav (str): Đường dẫn file WAV gốc.
        output_wav (str): Đường dẫn file WAV sau khi cắt.
        start_time (float): Thời gian bắt đầu (tính bằng giây).
        end_time (float): Thời gian kết thúc (tính bằng giây).
    """
    duration = end_time - start_time
    if duration <= 0:
        raise ValueError("end_time phải lớn hơn start_time")

    cmd = [
        "ffmpeg",
        "-i", input_wav,
        "-ss", str(start_time),
        "-t", str(duration),
        "-acodec", "copy",  # copy codec để không encode lại (nhanh hơn)
        output_wav
    ]

    subprocess.run(cmd, check=True)

# Ví dụ dùng:
# trim_wav_file("../tmp/audio_only.wav", "../tmp/audio_only2.wav", 1, 21)

trim_wav_file("../tmp/mixed_snr5.wav", "../tmp/mixed_snr5_5s.wav", 6, 11)
