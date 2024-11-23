from torch.utils.data import Dataset
from pathlib import Path
import cv2
from torchvision.transforms import Compose

from depth_anything.util.transform import Resize, NormalizeImage, PrepareForNet

class DepthDataset(Dataset):
    def __init__(self, image_path, transform=None):
        self.image_path = Path(image_path)
        self.transform = transform

        if self.image_path.is_file():
            if self.image_path.suffix == '.txt':
                with open(self.image_path, 'r') as f:
                    self.image_list = f.readlines()
            elif self.image_path.suffix in ['.png', '.jpg', '.jpeg']:
                self.image_list = [self.image_path]
        elif self.image_path.is_dir():
            self.image_list = []
            self.image_list.extend(Path(self.image_path).glob('*.png'))
            self.image_list.extend(Path(self.image_path).glob('*.jpg'))
            self.image_list.extend(Path(self.image_path).glob('*.jpeg'))
        
        if self.transform is None:
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

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image_path = self.image_list[idx]

        image = cv2.imread(str(image_path))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) / 255.0

        if self.transform:
            image = self.transform({'image': image})
            image = image['image']

        return image