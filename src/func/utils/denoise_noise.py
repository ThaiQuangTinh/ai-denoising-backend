import torch
import soundfile as sf
import numpy as np
from scipy.signal import stft, istft

def denoise_wav_file(model, noisy_wav_path, mean, std, output_path, device='cpu'):
    # Load noisy audio
    noisy, sr = sf.read(noisy_wav_path)

    # STFT
    f, t, Zxx = stft(noisy, fs=sr, nperseg=512)
    magnitude = np.abs(Zxx)
    phase = np.angle(Zxx)

    # Normalize
    mag_input = (magnitude - mean) / std
    mag_input = torch.tensor(mag_input, dtype=torch.float32).unsqueeze(0).unsqueeze(0).to(device)  # [B, C, F, T]

    # Denoise
    with torch.no_grad():
        mag_denoised = model(mag_input).squeeze().cpu().numpy()

    # Rescale
    mag_denoised = mag_denoised * std + mean

    # ISTFT
    Zxx_denoised = mag_denoised * np.exp(1j * phase)
    _, clean = istft(Zxx_denoised, fs=sr, nperseg=512)

    # Save output
    sf.write(output_path, clean, sr)
    print(f"✅ Denoised file saved to: {output_path}")



def denoise_long_wav_file(model, noisy_path, mean, std, output_path, segment_sec=5, device='cpu'):
    noisy, sr = sf.read(noisy_path)
    segment_samples = segment_sec * sr
    total_samples = len(noisy)

    clean_total = []

    for start in range(0, total_samples, segment_samples):
        end = min(start + segment_samples, total_samples)
        segment = noisy[start:end]

        # Lưu tạm đoạn nhỏ
        tmp_path = "./tmp_segment.wav"
        sf.write(tmp_path, segment, sr)

        # Denoise đoạn này
        tmp_output = "./tmp_segment_out.wav"
        denoise_wav_file(model, tmp_path, mean, std, tmp_output, device=device)

        # Load kết quả và thêm vào danh sách
        clean_seg, _ = sf.read(tmp_output)
        clean_total.append(clean_seg)

    # Ghép tất cả đoạn clean lại
    full_clean = np.concatenate(clean_total)
    sf.write(output_path, full_clean, sr)
    print(f"✅ Full denoised audio saved to: {output_path}")


