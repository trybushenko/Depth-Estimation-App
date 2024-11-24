# src/backend/api/main.py

import base64
import logging
import os
from io import BytesIO
from pathlib import Path

import cv2
import numpy as np
import torch
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from pydantic import BaseModel

from src.backend.models.depth_model import predict_depth
from src.depth_estimation.estimation_model import DepthModel

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
        depth_image = Image.fromarray(depth_map, mode="RGB")

        # Save the image to a buffer
        buffered = BytesIO()
        depth_image.save(buffered, format="PNG")
        depth_map_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        logging.info("Depth map encoded successfully")
    except Exception as e:
        logging.error(f"Error in depth prediction: {e}")
        raise HTTPException(status_code=500, detail="Depth prediction failed")

    return {"depth_map": depth_map_base64}
