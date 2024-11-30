# src/backend/api/main.py

import base64
import logging
from io import BytesIO

import requests
from fastapi import FastAPI, File, Form
from typing import Optional

from fastapi import HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

from src.backend.models.depth_model import predict_depth
from src.backend.models.lvlm_model import generate_response

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


# from transformers import AutoModelForCausalLM, AutoTokenizer
# from huggingface_hub import login

# from PIL import Image
# import os
# import dotenv
# import torch


# # Load environment variables from .env
# dotenv.load_dotenv()

# hf_token = os.getenv('HUGGING_FACE_TOKEN')
# if hf_token:
#     try:
#         login(token=hf_token)
#         print("Successfully logged into Hugging Face.")
#     except Exception as e:
#         print(f"Failed to log into Hugging Face: {e}")
#         # Handle the error as needed
# else:
#     print("Hugging Face token not provided. Skipping login.")
# # Save Hugging Face token if provided
# # if os.getenv("HF_token"):
# #     access_token = os.getenv("HF_token")
# #     HfFolder.save_token(access_token)

# # Initialize logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Load model at startup
# device = 'cuda' if torch.cuda.is_available() else 'cpu'
# model_name = 'RussRobin/SpatialBot-3B'

# global model
# logger.info(f"Loading model '{model_name}' on device '{device}'...")
# model = AutoModelForCausalLM.from_pretrained(
#     model_name,
#     torch_dtype=torch.float16 if device == 'cuda' else torch.float32,
#     device_map='auto',
#     trust_remote_code=True
# )
# tokenizer = AutoTokenizer.from_pretrained(
#     model_name,
#     trust_remote_code=True
# )


# Add the new endpoint
@app.post("/depthgpt")
async def depth_gpt(
    file: UploadFile = File(...),
    prompt: str = Form(...),
):
    """
    Handle DepthGPT functionality by processing the image, generating depth map,
    and interacting with the LVLM model.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")

    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    try:
        # Read the image bytes
        image_bytes = await file.read()

        # Convert the original image bytes to a PIL Image
        original_image = Image.open(BytesIO(image_bytes)).convert('RGB')

        # Predict depth map
        depth_map = predict_depth(image_bytes)

        # Convert depth map to PIL Image
        depth_image = Image.fromarray(depth_map, mode="RGB")

        # Prepare images list for generate_response
        images_list = [original_image, depth_image]

        # Generate response from LVLM model
        lvlm_output = generate_response(prompt, images_list)

        # Encode images to base64 for frontend display
        depth_buffered = BytesIO()
        depth_image.save(depth_buffered, format="PNG")
        depth_map_base64 = base64.b64encode(depth_buffered.getvalue()).decode("utf-8")

        rgb_buffered = BytesIO()
        original_image.save(rgb_buffered, format="PNG")
        rgb_image_base64 = base64.b64encode(rgb_buffered.getvalue()).decode("utf-8")

        return {
            "lvlm_response": lvlm_output['response'],
            "depth_map": depth_map_base64,
            "rgb_image": rgb_image_base64,
        }
    except Exception as e:
        logging.error(f"Error in depth_gpt: {e}")
        raise HTTPException(status_code=500, detail="DepthGPT processing failed")
    

from typing import List

@app.post("/analyze")
async def analyze_image(prompt: str = Form(...), images: List[UploadFile] = File(...)):

    image_list = []
    for image_file in images:
        image_bytes = await image_file.read()
        image = Image.open(BytesIO(image_bytes)).convert('RGB')
        image_list.append(image)

    response = generate_response(prompt, image_list)




    

    