from pathlib import Path

import cv2
from depth_estimation.depth_anything.util.transform import NormalizeImage, PrepareForNet, Resize
from torch.utils.data import Dataset
from torchvision.transforms import Compose


class DepthDataset(Dataset):
    def __init__(self, image_path, transform=None):
        self.image_path = Path(image_path)
        self.transform = transform

        if self.image_path.is_file():
            if self.image_path.suffix == ".txt":
                with open(self.image_path, "r") as f:
                    self.image_list = f.readlines()
            elif self.image_path.suffix in [".png", ".jpg", ".jpeg"]:
                self.image_list = [self.image_path]
        elif self.image_path.is_dir():
            self.image_list = []
            self.image_list.extend(Path(self.image_path).glob("*.png"))
            self.image_list.extend(Path(self.image_path).glob("*.jpg"))
            self.image_list.extend(Path(self.image_path).glob("*.jpeg"))

    def __len__(self):
        return len(self.image_list)

    def __getitem__(self, idx):
        image_path = self.image_list[idx]

        image = cv2.imread(str(image_path))

        return image
