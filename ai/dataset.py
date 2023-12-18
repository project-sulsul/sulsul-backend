from glob import glob
from PIL import Image
from typing import *

import torch
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader, Dataset

"""
path: ./dataset/
├── images
│    ├─ class 1
│        ├─ img1.jpg
│        ├─ ...
│    ├─ class 2
│        ├─ img1.jpg
│        ├─ ...
│    ├─ class 3
│        ├─ img1.jpg
│        ├─ ...
│    ├─ class 4
│        ├─ img1.jpg
│        ├─ ...
│    ├─ ...
│        ├─ ...
│        ├─ ...
"""

class_info = {
    # foods
    'beef': 0, 'chicken': 1, 'chicken_feet': 2, 'chicken_ribs': 3, 'dry_snacks': 4,
    'dubu_kimchi': 5, 'ecliptic': 6, 'egg_roll': 7, 'fish_cake_soup': 8,
    'french_fries': 9, 'gopchang': 10, 'hwachae': 11, 'jjambbong': 12,
    'jjapageti': 13, 'korean_ramen': 14, 'lamb_skewers': 15, 'nacho': 16,
    'nagasaki': 17, 'pizza': 18, 'pork_belly': 19, 'pork_feet': 20,
    'raw_meat': 21, 'salmon': 22, 'sashimi': 23, 'shrimp_tempura': 24,
    
    # drinks
    'beer': 25, 'cass': 26, 'chamisul_fresh': 27, 'chamisul_origin': 28,
    'chum_churum': 29, 'highball': 30, 'hite': 31, 'jinro': 32, 'kelly': 33, 
    'kloud': 34, 'ob': 35, 'saero': 36, 'soju': 37, 'tera': 38,
}

# image padding to prevent distortion of image
class Padding(object):

    def __init__(self, fill):
        self.fill = fill

    def __call__(self, src):
        w, h = src.size

        if w == h:
            return src
        elif w > h:
            out = Image.new(src.mode, (w, w), self.fill)
            out.paste(src, (0, (w - h) // 2))
            return out
        else:
            out = Image.new(src.mode, (h, h), self.fill)
            out.paste(src, ((h - w) // 2, 0))
            return out


class CustomDataset(Dataset):
    def __init__(
        self, 
        path: str, 
        subset: str='train', 
        num_classes: int=39, 
        transform=None,
    ):

        self.image_files = glob(path+subset+'/*.jpg')
        label_files = [file.replace('.jpg', '.txt') for file in self.image_files]
        self.labels = self.read_labels(label_files)
        self.transform = transform
        self.num_classes = num_classes
        
    def __len__(self):
        return len(self.image_files)
    
    def __getitem__(self, idx):
        image = Image.open(self.image_files[idx]).convert('RGB')
        label = torch.zeros(self.num_classes)
        cls_idx = self.labels[idx]
        label[cls_idx] = 1
        return self.transform(image), label
        
    def read_labels(self, label_files):
        label_list = []
        for file in label_files:
            with open(file, 'r') as f:
                lines = f.readlines()
        
            labels = []
            for line in lines:
                line = line.strip().split()
                label = [class_info[x] for x in line]    
                labels.append(label)
            label_list.append(sum(labels, []))
        return label_list


def load_dataloader(
    path: str,
    img_size: int=224,
    fill_color: Tuple[int, int, int]=(0, 0, 0),
    subset: str='train',
    num_classes: int=39,
    num_workers: int=8,
    batch_size: int=32,
    shuffle: bool=True,
    drop_last: bool=True,
):
    assert subset in ('train', 'valid', 'test')

    if subset == 'train':
        augmentation = [
            Padding(fill=fill_color),
            transforms.Resize((img_size, img_size)),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(degrees=(-20, 20)),
            transforms.ToTensor(),
        ]
    
    else:
        augmentation = [
            Padding(fill=fill_color),
            transforms.Resize((img_size, img_size)),
            transforms.ToTensor(),
        ]    
        
    augmentation.append(
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    )
    
    augmentation = transforms.Compose(augmentation)

    data_loader = DataLoader(
        CustomDataset(path=path, subset=subset, transform=augmentation, num_classes=num_classes),
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        drop_last=drop_last,
    )

    return data_loader