import cv2
import os
from pathlib import Path

import numpy as np
import torch
from loguru import logger
from PIL import Image

from src.depth_estimation.estimation_model import DepthModel

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.info(f"Using device: {device}")

# Adjust the root path as necessary
# root_path = Path(__file__).resolve().parents[3]
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


@torch.no_grad()
def predict_depth(image_bytes_io):
    try:

        img_array = np.frombuffer(image_bytes_io, dtype=np.uint8)
        image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        prediction = model.infer([image])[0]

        # Log prediction details
        logger.info(f"Depth map shape: {prediction.shape}")

        return prediction
    except Exception as e:
        logger.error(f"Error in predict_depth: {e}")
        raise
