import torch
import torch.nn.functional as F
import numpy as np
import cv2
import re
from pathlib import Path
from typing import List

from torchvision.transforms import Compose

from src.depth_estimation.depth_anything.util.transform import Resize, NormalizeImage, PrepareForNet


from src.depth_estimation.depth_anything.dpt import DepthAnything

class DepthModel:
    def __init__(self, model_name, device: str | torch.device, model_load_dir: str | Path, grayscale: bool = False):
        
        if isinstance(device, str) and device == 'cuda' and not torch.cuda.is_available():
            raise ValueError("CUDA is not available. Please check your CUDA installation.")
        
        if isinstance(device, str):
            device = torch.device(device)
        
        self.model_name = model_name
        self.device = device

        self.model_load_dir = Path(model_load_dir)

        self.version = self._get_version()
        self.encoder = self._get_encoder()
        
        self.model = self._load_model()
        self.model.eval()
        self.model = self.model.to(device=self.device)
        
        self.total_params = sum(p.numel() for p in self.model.parameters()) / 1e6  # In millions

        self.grayscale = grayscale

        self.transform = Compose([
            Resize(width=518,
                    height=518,
                    resize_target=False,
                    keep_aspect_ratio=True,
                    ensure_multiple_of=14,
                    resize_method='lower_bound',
                    image_interpolation_method=cv2.INTER_CUBIC,
                ),
            NormalizeImage(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            PrepareForNet(),
        ])

    def _get_version(self):
        match = re.search(r'v(1|2)', self.model_name.lower())
        if match:
            return f'v{match.group(1)}'
        raise ValueError("Invalid version specified. Please specify either v1 or v2.")
    
    def _get_encoder(self):
        # Option 1: Using re.search
        match = re.search(r'vit(s|b|l)', self.model_name.lower())
        if match:
            return f'vit{match.group(1)}'
        raise ValueError("Invalid encoder specified. Please specify either vits, vitb, or vitl.")


    def _load_model(self):
        
        model_configs = {
            'vits': {'encoder': 'vits', 'features': 64, 'out_channels': [48, 96, 192, 384]},
            'vitb': {'encoder': 'vitb', 'features': 128, 'out_channels': [96, 192, 384, 768]},
            'vitl': {'encoder': 'vitl', 'features': 256, 'out_channels': [256, 512, 1024, 1024]},
        }
        model = DepthAnything(**model_configs[self.encoder])
        model_path = self.model_load_dir / f'depth_anything_{self.version}_{self.encoder}.pth'
        model.load_state_dict(torch.load(model_path, map_location='cpu', weights_only=True))
        return model.to(self.device).eval()

    def infer(self, images:List[np.ndarray]) -> np.ndarray:
        depth_maps = []

        if type(images) != list:
            raise TypeError("Input must be a list of images.")
        
        for image in images:
            if image.ndim != 3:
                raise ValueError("Input image must have 3 channels.")
            
            depth = self.model.infer_image(image)

            depth_map_normalized = depth / np.max(depth)

            depth_map_uint8 = (depth_map_normalized * 255).astype("uint8")
            depth_map_uint8 = depth_map_uint8.squeeze()

            if self.grayscale:
                depth = np.repeat(depth_map_uint8[..., np.newaxis], 3, axis=-1)

            else:
                depth = cv2.applyColorMap(depth_map_uint8, cv2.COLORMAP_VIRIDIS)

            depth_maps.append(depth)
        
        return depth_maps