import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image
from typing import List
import io
import logging
import dotenv
import os
from huggingface_hub import login

from PIL import Image

import time

# Load environment variables from .env
dotenv.load_dotenv()

hf_token = os.getenv('HUGGING_FACE_TOKEN')
if hf_token:
    try:
        login(token=hf_token)
        print("Successfully logged into Hugging Face.")
    except Exception as e:
        print(f"Failed to log into Hugging Face: {e}")
        # Handle the error as needed
else:
    print("Hugging Face token not provided. Skipping login.")

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load model at startup
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model_name = 'RussRobin/SpatialBot-3B'

logger.info(f"Loading model '{model_name}' on device '{device}'...")
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16 if device == 'cuda' else torch.float32,
    device_map='auto',
    trust_remote_code=True
)
tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    trust_remote_code=True
)

logger.info("Model loaded successfully.")

# @app.post("/analyze")
def generate_response(prompt: str, images: List[Image.Image]):
    """
    Analyze images and respond to the prompt using the LVLM model.

    Expects two images: RGB image and Depth map.
    """

    try:
        if len(images) != 2:
            logger.error("Incorrect number of images received.")
            return {"error": "Two images (RGB and Depth map) are required."}

        global model
        # Process images
        logger.info("Processing images...")
        image_tensor = model.process_images(images, model.config).to(dtype=model.dtype, device=device)

        # Construct the prompt
        text = (
            "A chat between a curious user and an artificial intelligence assistant. "
            "The assistant gives helpful, detailed, and polite answers to the user's questions. "
            f"USER: <image 1>\n<image 2>\n{prompt} ASSISTANT:"
        )
        logger.info(f"Constructed prompt: {text}")


        # Tokenize the prompt
        text_chunks = [tokenizer(chunk).input_ids for chunk in text.split('<image 1>\n<image 2>\n')]
        input_ids = torch.tensor(
            text_chunks[0] + [-201] + [-202] + text_chunks[1],
            dtype=torch.long
        ).unsqueeze(0).to(device)

        # Ensure the model and input are on the same device
        logger.info("Moving model and input to device...")
        input_ids = input_ids.cuda()
        image_tensor = image_tensor.cuda()
        model = model.cuda()
        
        # Generate the response
        logger.info("Generating response from LVLM model...")
        output_ids = model.generate(
            input_ids,
            images=image_tensor,
            max_new_tokens=100,
            use_cache=True,
            repetition_penalty=1.0
        )[0]
        
        # Decode the response
        logger.info("Decoding response...")
        response_text = tokenizer.decode(
            output_ids[input_ids.shape[1]:],
            skip_special_tokens=True
        ).strip()


        logger.info(f"Generated response: {response_text}")

        return {"response": response_text}

    except Exception as e:
        logger.error(f"Error in generate_response: {e}")
        return {"error": str(e)}