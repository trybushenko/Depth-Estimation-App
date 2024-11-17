# src/backend/api/main.py

from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from io import BytesIO
from PIL import Image
import numpy as np
import base64
import logging
import torch

from src.backend.models.depth_model import predict_depth


class ImageBase64(BaseModel):
    image: str  # Base64-encoded image string

app = FastAPI(title="Depth Estimation API")

origins = [
    "http://localhost:3000",  # Frontend origin
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
    "image/webp"
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
    content_type = request.headers.get('Content-Type', '')

    if 'multipart/form-data' in content_type:
        # Handle file upload
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")
        # Check MIME type
        if file.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        # Read image bytes
        image_bytes = await file.read()
    elif 'application/json' in content_type:
        # Handle base64-encoded image
        try:
            data = await request.json()
            image_base64 = data.get('image')
            if not image_base64:
                raise HTTPException(status_code=400, detail="No image provided in JSON")
            # Decode base64 image
            image_bytes = base64.b64decode(image_base64)
        except Exception as e:
            logging.error(f"Error parsing JSON: {e}")
            raise HTTPException(status_code=400, detail="Invalid JSON input")
    else:
        raise HTTPException(status_code=415, detail="Unsupported Media Type")

    try:
        # Create a BytesIO object from image bytes
        image_bytes_io = BytesIO(image_bytes)
    except Exception as e:
        logging.error(f"Error processing image bytes: {e}")
        raise HTTPException(status_code=400, detail="Invalid image data")

    # Predict the depth map by passing the file-like object
    try:
        depth_map = predict_depth(image_bytes_io)
    except Exception as e:
        logging.error(f"Error in depth prediction: {e}")
        raise HTTPException(status_code=500, detail="Depth prediction failed")

    # Convert depth map to base64-encoded PNG image
    try:
        # Normalize the depth map to range [0, 255]
        if np.max(depth_map) != 0:
            depth_map_normalized = depth_map / np.max(depth_map)
        else:
            depth_map_normalized = depth_map  # Avoid division by zero

        depth_map_uint8 = (depth_map_normalized * 255).astype('uint8')

        # Remove singleton dimensions if any
        depth_map_uint8 = np.squeeze(depth_map_uint8)

        # Determine the image mode based on array dimensions
        if depth_map_uint8.ndim == 2:
            mode = 'L'  # Grayscale
        elif depth_map_uint8.ndim == 3 and depth_map_uint8.shape[0] == 3:
            depth_map_uint8 = depth_map_uint8.transpose(1, 2, 0)  # Convert to (H, W, C)
            mode = 'RGB'
        else:
            raise ValueError(f"Unsupported depth_map shape: {depth_map_uint8.shape}")

        # Convert the NumPy array to a PIL Image
        depth_image = Image.fromarray(depth_map_uint8, mode=mode)

        # Save the image to a buffer
        buffered = BytesIO()
        depth_image.save(buffered, format="PNG")
        depth_map_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        logging.info("Depth map encoded successfully")
    except Exception as e:
        logging.error(f"Error encoding depth map: {e}")
        raise HTTPException(status_code=500, detail="Failed to encode depth map")

    return {"depth_map": depth_map_base64}
