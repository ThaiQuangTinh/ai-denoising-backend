import os
import subprocess

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


def concat_wav_files(wav_files, output_file, tmp_list_file="file_list.txt"):
    """
    Gộp nhiều file WAV thành một file WAV duy nhất bằng ffmpeg.

    Parameters:
        wav_files (list of str): Danh sách các file WAV cần gộp.
        output_file (str): Tên file WAV đầu ra.
        tmp_list_file (str): Tên file tạm chứa danh sách các file WAV (dùng cho ffmpeg).
    """
    # Tạo nội dung cho file danh sách
    with open(tmp_list_file, "w", encoding="utf-8") as f:
        for file in wav_files:
            f.write(f"file '{file}'\n")  # ffmpeg yêu cầu dòng: file 'filename'

    # Gọi ffmpeg để gộp các file
    cmd = [
        "ffmpeg",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        tmp_list_file,
        "-c",
        "copy",
        output_file,
    ]

    subprocess.run(cmd, check=True)

    # Xoá file tạm
    os.remove(tmp_list_file)


# Ví dụ dùng:
concat_wav_files(
    [
        "../../data/noise/noise_121.wav",
        "../../data/noise/noise_145.wav",
        "../../data/noise/noise_064.wav",
        "../../data/noise/noise_040.wav",
        "../../data/noise/noise_037.wav",
        "../../data/noise/noise_031.wav",
    ],
    "../tmp/merge_wav_nosie.wav",
)
