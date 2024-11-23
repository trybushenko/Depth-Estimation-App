# src/backend/api/main.py

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from io import BytesIO
import base64
import logging
from PIL import Image
import cv2
import numpy as np
import torch

import os
from pathlib import Path

from src.depth_estimation.estimation_model import DepthModel
from src.backend.models.depth_model import predict_depth

app = FastAPI(title="Depth Estimation API")

origins = [
    "http://localhost:8080",  # Frontend origin
    # Add other allowed origins if necessary
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Adjust this to your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_MIME_TYPES = [
    "image/jpeg",
    "image/png",
    "image/jpg",
    "image/gif",
    "image/bmp",
    "image/tiff",
    "image/webp",
]

# Load the model at startup
@app.on_event("startup")
async def startup_event():
    global model, device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    weights_path_dict = {
        "vits": Path(os.getcwd()) / "tmp/model-weights/depth_anything_v2_vits.pth",
        "vitb": Path(os.getcwd()) / "tmp/model-weights/depth_anything_v2_vitb.pth",
        "vitl": Path(os.getcwd()) / "tmp/model-weights/depth_anything_v2_vitl.pth",
    }

    model_configs = {
        "vits": {"encoder": "vits", "features": 64, "out_channels": (48, 96, 192, 384)},
        "vitb": {"encoder": "vitb", "features": 128, "out_channels": (96, 192, 384, 768)},
        "vitl": {
            "encoder": "vitl",
            "features": 256,
            "out_channels": (256, 512, 1024, 1024),
        },
        "vitg": {
            "encoder": "vitg",
            "features": 384,
            "out_channels": (1536, 1536, 1536, 1536),
        },
    }


    # Load the model at startup
    model = DepthModel('v2_vits',
                    device='cuda',
                    model_load_dir=Path(os.getcwd()) / 'tmp/model-weights/', 
                    grayscale=False)
    

@app.post("/predict")
async def predict_depth_map(
    file: UploadFile = File(None),
):
    """
    Predict the depth map from an input image.

    This endpoint accepts image files via multipart/form-data.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    try:
        image_bytes = await file.read()

        depth_map = predict_depth(image_bytes)
        
        # Encode depth map to PNG and then to base64
        depth_image = Image.fromarray(depth_map, mode='RGB')

        # Save the image to a buffer
        buffered = BytesIO()
        depth_image.save(buffered, format="PNG")
        depth_map_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        logging.info("Depth map encoded successfully")
    except Exception as e:
        logging.error(f"Error in depth prediction: {e}")
        raise HTTPException(status_code=500, detail="Depth prediction failed")
    
    return {"depth_map": depth_map_base64}
