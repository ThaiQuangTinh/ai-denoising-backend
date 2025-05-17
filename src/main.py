import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

import logging
import uuid, shutil, torch

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi import BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from src.model import UNetEnhanced
from src.model_inference import denoise_long_wav_file
from src.utils import merge_video_audio, split_video_audio


# Logging configuration (log to terminal)
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',  
                    stream=sys.stdout) 

logging.info("Server is starting...")

# Load model
model_path = "./model/unet_speech_denoising_best.pth"
stats_path = '../data/features/train_mag_stats.pt'

# Load mean and std
stats = torch.load(stats_path)
mean = stats['mean']
std = stats['std']

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = UNetEnhanced()
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
model.to(device)

app = FastAPI()

# Alow frontend React access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/denoise_video")
async def denoise_video(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...), 
):
    logging.info("Received request to denoise video.")

    # Create temp folder for each request (base on uuid was random)
    request_id = str(uuid.uuid4())
    temp_dir = os.path.join("./temp", request_id)
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # Save original video
        input_path = os.path.join(temp_dir, "input.mp4")
        with open(input_path, "wb") as f:
            f.write(await file.read())

        logging.info(f"Original video saved at: {input_path}")

        # Temp files
        video_path = os.path.join(temp_dir, "video_only.mp4")
        audio_path = os.path.join(temp_dir, "audio.wav")
        clean_audio_path = os.path.join(temp_dir, "clean_audio.wav")
        output_path = os.path.join(temp_dir, "output.mp4")

        # 1. Split video and audio
        logging.info("Splitting video and audio...")
        split_video_audio(input_path, video_path, audio_path)

        # 2. Denoise audio
        logging.info("Denoising audio...")
        denoise_long_wav_file(model, audio_path, mean, std, clean_audio_path, device)

        # 3. Merge clean audio with video
        logging.info("Merging clean audio with video...")
        merge_video_audio(video_path, clean_audio_path, output_path)

        # # 4. Response result for client
        logging.info("Returning denoised video...")
        # background_tasks.add_task(shutil.rmtree, temp_dir, ignore_errors=True)
        return FileResponse(output_path, media_type="video/mp4", filename="denoised_output.mp4")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise e

    finally:
        logging.info("Temporary files deleted.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
