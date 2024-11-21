import os
from pathlib import Path

import numpy as np
import torch
from loguru import logger
from PIL import Image

from src.depth_estimation.depth_anything_v2.dpt import DepthAnythingV2

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


def load_model(model_type="vitb", device=device):
    weights_path = weights_path_dict[model_type]
    model = DepthAnythingV2(
        encoder=model_configs[model_type]["encoder"],
        features=model_configs[model_type]["features"],
        out_channels=model_configs[model_type]["out_channels"],
    )
    state_dict = torch.load(weights_path, map_location="cpu", weights_only=True)
    model.load_state_dict(state_dict, strict=True)
    model.eval()
    model.to(device)
    logger.info(f"Model {model_type} was successfully loaded into device: {device}")
    return model


# Load the model at startup
model = load_model(model_type="vits", device=device)


@torch.no_grad()
def predict_depth(image_bytes_io):
    try:

        try:
            image = Image.open(image_bytes_io).convert("RGB")
        except Exception as e:
            raise ValueError(f"Unable to open image: {e}")

        # Open the image from BytesIO
        # image = Image.open(image_bytes_io).convert('RGB')

        # Convert PIL Image to NumPy array
        image_np = np.array(image)

        # Log image details
        logger.info(
            f"predict_depth - Image type: {type(image_np)}, Image shape: {image_np.shape}"
        )

        # Pass the NumPy array to image2tensor
        processed_image, _ = model.image2tensor(image_np)

        # Move the processed image to the appropriate device
        processed_image = processed_image.to(device)

        # Perform prediction
        prediction = model(processed_image)

        # Log prediction details
        logger.info(f"Depth map shape: {prediction.shape}")

        return prediction.cpu().detach().numpy()
    except Exception as e:
        logger.error(f"Error in predict_depth: {e}")
        raise
