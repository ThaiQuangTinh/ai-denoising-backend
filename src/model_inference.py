import torchaudio
import torch
import os


# DENOISE ANY NOISY FILE

def denoise_wav_file(model, noisy_wav_path, mean, std, save_path, device):
    model.eval()

    # Load file wav
    wav, sr = torchaudio.load(noisy_wav_path)
    wav = wav.mean(dim=0)  # If stereo, mix to mono
    if sr != 16000:
        wav = torchaudio.functional.resample(wav, sr, 16000)

    # Calcualte STFT
    window = torch.hann_window(512).to(wav.device)
    stft = torch.stft(wav, n_fft=512, hop_length=128, win_length=512,
                      window=window, return_complex=True)  # (F, T)
    noisy_mag = torch.abs(stft)
    noisy_phase = torch.angle(stft)

    # Extraction magnitude
    noisy_mag_norm = (noisy_mag - mean) / std
    input_tensor = noisy_mag_norm.unsqueeze(0).unsqueeze(0).to(device)  # (1, 1, F, T)

    with torch.no_grad():
        denoised_mag_norm = model(input_tensor)

    # Denormalization
    denoised_mag = denoised_mag_norm.squeeze().cpu() * std + mean  # (F, T)

    # Create complex spec
    real = denoised_mag * torch.cos(noisy_phase)
    imag = denoised_mag * torch.sin(noisy_phase)
    complex_spec = torch.complex(real, imag)

    # ISTFT
    denoised_waveform = torch.istft(
        complex_spec,
        n_fft=512,
        hop_length=128,
        win_length=512,
        window=torch.hann_window(512),
        length=wav.shape[0]  # để đảm bảo khôi phục đúng chiều dài
    )

    # Write to wav file
    torchaudio.save(save_path, denoised_waveform.unsqueeze(0), sample_rate=16000)
    print(f"✅ File denoised đã lưu tại: {save_path}")


import torchaudio
import torch
import os
import tempfile
from tqdm import tqdm

def denoise_long_wav_file(model, noisy_path, mean, std, output_path, device='cpu', segment_sec=5):
    model.eval()

    # Load file, chuyển về 16kHz và mono nếu cần
    wav, sr = torchaudio.load(noisy_path)
    wav = wav.mean(dim=0)
    if sr != 16000:
        wav = torchaudio.functional.resample(wav, sr, 16000)
        sr = 16000

    segment_len = segment_sec * sr
    total_len = wav.shape[0]
    denoised_segments = []
    
    # Tính số đoạn cần xử lý
    num_segments = (total_len + segment_len - 1) // segment_len

    # Vòng lặp xử lý từng đoạn với thanh tiến trình tqdm
    for start in tqdm(range(0, total_len, segment_len), desc="Processing segments", total=num_segments):
        end = min(start + segment_len, total_len)
        chunk = wav[start:end]

        # Nếu đoạn cuối có độ dài nhỏ hơn, thêm zero-padding để đủ 5s
        if chunk.shape[0] < segment_len:
            pad_len = segment_len - chunk.shape[0]
            chunk = torch.cat([chunk, torch.zeros(pad_len)])

        # Lưu đoạn tạm ra file (sử dụng tempfile để tránh xung đột tên file)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_in:
            torchaudio.save(tmp_in.name, chunk.unsqueeze(0), sample_rate=sr)
            tmp_in_path = tmp_in.name

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_out:
            tmp_out_path = tmp_out.name

        # Xử lý denoise từng đoạn
        denoise_wav_file(model, tmp_in_path, mean, std, tmp_out_path, device)

        # Load lại đoạn denoise
        denoised_chunk, _ = torchaudio.load(tmp_out_path)
        denoised_segments.append(denoised_chunk.squeeze(0))

        # Xoá file tạm
        os.remove(tmp_in_path)
        os.remove(tmp_out_path)

    # Ghép tất cả các đoạn lại thành 1 file
    full_denoised = torch.cat(denoised_segments)[:total_len]  # Cắt bớt nếu có zero-padding dư
    torchaudio.save(output_path, full_denoised.unsqueeze(0), sample_rate=sr)
    print(f"🎉 File denoised toàn bộ đã lưu tại: {output_path}")
