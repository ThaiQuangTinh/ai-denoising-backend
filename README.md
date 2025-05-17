# AI Speech Denoising Backend

This project is an AI-based backend application for speech denoising, designed to remove noise from audio and video files using a deep learning model (UNet). The project is organized as follows:

## Directory Structure

- **data/**
  - **clean/**: Contains clean speech audio files.
  - **noise/**: Contains noise audio files (e.g., wind, water, traffic, etc.).
  - **noisy/**: Contains mixed audio files (clean speech + noise).
  - **features/**: Stores extracted audio features (e.g., STFT, magnitude, phase).
  - **splits/**: Contains dataset splits for training, validation, and testing (CSV files).

- **src/**
  - **main.py**: Main entry point of the application. Run this file to start the backend server.
  - **model.py**: Implementation of the UNet model for speech denoising.
  - **model_inference.py**: Functions for denoising audio using the trained model.
  - **utils.py**: Utility functions (e.g., split audio from video, merge audio into video).
  - **chart/**: Scripts for generating evaluation charts and visualizations.
  - **func/**: Data processing, model training, and evaluation scripts.
  - **model/**: Stores trained model files.
  - **temp/**: Temporary files generated during the denoising process (e.g., intermediate audio/video files).

## How to Use

1. **Download Data**  
   The `data/` and `model/unet_speech_denoising_best.pth` folders can be downloaded from Google Drive:  
   [Download Link](https://drive.google.com/drive/folders/1Jgpha4WBP0ULhCjd5ho7C1sjcT6_kOQ9?usp=drive_link)

2. **Run the Application**  
   Start the backend server by running:
   ```sh
   python src/main.py