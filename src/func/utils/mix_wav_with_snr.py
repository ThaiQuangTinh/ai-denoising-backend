import numpy as np
import soundfile as sf
import subprocess
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


def resample_wav(input_path, output_path, target_sr=16000):
    cmd = [
        "ffmpeg",
        "-y",  # Ghi đè nếu file đã tồn tại
        "-i",
        input_path,
        "-ar",
        str(target_sr),  # Set sample rate
        output_path,
    ]
    subprocess.run(cmd, check=True)
    print(f"✅ Resampled: {input_path} → {output_path}")


def mix_with_snr(clean_path, noise_path, output_path, snr_db=5):
    # Resample cả 2 file
    # resample_wav(clean_path, clean_resampled, target_sr)
    # resample_wav(noise_path, noise_resampled, target_sr)

    # Đọc tín hiệu sau khi resample
    clean, sr = sf.read(clean_path)
    noise, sr_noise = sf.read(noise_path)

    assert sr == sr_noise, "Sample rates must match"

    # Cắt hoặc lặp noise để match độ dài
    if len(noise) < len(clean):
        repeat_times = int(np.ceil(len(clean) / len(noise)))
        noise = np.tile(noise, repeat_times)
    noise = noise[: len(clean)]

    # Tính công suất
    power_clean = np.mean(clean**2)
    power_noise = np.mean(noise**2)
    target_noise_power = power_clean / (10 ** (snr_db / 10))
    scale = np.sqrt(target_noise_power / power_noise)

    # Mix và chuẩn hóa
    mixed = clean + noise * scale
    max_val = np.max(np.abs(mixed))
    if max_val > 1:
        mixed = mixed / max_val

    # Ghi ra file
    sf.write(output_path, mixed, sr)
    print(f"✅ Mixed audio saved to: {output_path}")


# Ví dụ dùng
mix_with_snr(
    clean_path='../tmp/audio.wav',
    noise_path="../tmp/merge_wav_nosie.wav",
    output_path="../tmp/mixed_snr5.wav",
    snr_db=5
)
