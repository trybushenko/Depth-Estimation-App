# src/backend/api/main.py

import base64
import logging
from io import BytesIO
import cv2

import numpy as np
import torch
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from pydantic import BaseModel

from src.backend.models.depth_model import predict_depth


class ImageBase64(BaseModel):
    image: str  # Base64-encoded image string


app = FastAPI(title="Depth Estimation API")

origins = [
    "http://localhost:8080",  # Frontend origin
    # Add other allowed origins if necessary
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Adjust this to your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define allowed MIME types
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
    request: Request,
    file: UploadFile = File(None),
):
    """
    Predict the depth map from an input image.

    This endpoint accepts either a file upload or a base64-encoded image in JSON.
    """

    # Check the content type
    content_type = request.headers.get("Content-Type", "")

    if "multipart/form-data" in content_type:
        # Handle file upload
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")
        # Check MIME type
        if file.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        # Read image bytes
        image_bytes = await file.read()
    elif "application/json" in content_type:
        # Handle base64-encoded image
        try:
            data = await request.json()
            image_base64 = data.get("image")
            if not image_base64:
                raise HTTPException(status_code=400, detail="No image provided in JSON")
            # Decode base64 image
            image_bytes = base64.b64decode(image_base64)
        except Exception as e:
            logging.error(f"Error parsing JSON: {e}")
            raise HTTPException(status_code=400, detail="Invalid JSON input")
    else:
        raise HTTPException(status_code=415, detail="Unsupported Media Type")

    # Predict the depth map by passing the file-like object
    try:
        depth_map = predict_depth(image_bytes)

    except Exception as e:
        logging.error(f"Error in depth prediction: {e}")
        raise HTTPException(status_code=500, detail="Depth prediction failed")

    # Convert depth map to base64-encoded PNG image
    try:
        
        depth_image = Image.fromarray(depth_map, mode='RGB')

        # Save the image to a buffer
        buffered = BytesIO()
        depth_image.save(buffered, format="PNG")
        depth_map_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        logging.info("Depth map encoded successfully")
    except Exception as e:
        logging.error(f"Error encoding depth map: {e}")
        raise HTTPException(status_code=500, detail="Failed to encode depth map")

    return {"depth_map": depth_map_base64}
