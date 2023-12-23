from glob import glob
from typing import *

from PIL import Image
from torch import zeros
from torch.utils.data import DataLoader, Dataset
from torchvision.transforms import Compose, Resize, ToTensor, Normalize, RandomRotation, RandomHorizontalFlip

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
    "beef": 0,  # 소고기
    "chicken": 1,  # 치킨
    "chicken_feet": 2,  # 닭발
    "chicken_ribs": 3,  # 닭갈비
    "dry_snacks": 4,  # 마른 안주
    "dubu_kimchi": 5,  # 두부 김치
    "ecliptic": 6,  # 황도
    "egg_roll": 7,  # 계란말이
    "fish_cake_soup": 8,  # 어묵탕
    "french_fries": 9,  # 감자 튀김
    "gopchang": 10,  # 곱창
    "hwachae": 11,  # 화채
    "jjambbong": 12,  # 짬뽕
    "jjapageti": 13,  # 짜파게티
    "korean_ramen": 14,  # 라면
    "lamb_skewers": 15,  # 양꼬치
    "nacho": 16,  # 나초
    "nagasaki": 17,  # 나가사키 짬뽕
    "pizza": 18,  # 피자
    "pork_belly": 19,  # 삼겹살
    "pork_feet": 20,  # 족발
    "raw_meat": 21,  # 육회
    "salmon": 22,  # 연어
    "sashimi": 23,  # 회
    "shrimp_tempura": 24,  # 새우튀김
    # drinks
    "beer": 25,  # 맥주
    "cass": 26,  # 카스
    "chamisul_fresh": 27,  # 참이슬 후레쉬
    "chamisul_origin": 28,  # 참이슬 오리지널
    "chum_churum": 29,  # 처음처럼
    "highball": 30,  # 하이볼
    "hite": 31,  # 하이트
    "jinro": 32,  # 진로
    "kelly": 33,  # 켈리
    "kloud": 34,  # 클라우드
    "ob": 35,  # OB
    "saero": 36,  # 새로
    "soju": 37,  # 소주
    "tera": 38,  # 테라
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
        subset: str = "train",
        num_classes: int = 39,
        transform=None,
    ):
        self.image_files = glob(path + subset + "/*.jpg")
        label_files = [file.replace(".jpg", ".txt") for file in self.image_files]
        self.labels = self.read_labels(label_files)
        self.transform = transform
        self.num_classes = num_classes

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        image = Image.open(self.image_files[idx]).convert("RGB")
        label = zeros(self.num_classes)
        cls_idx = self.labels[idx]
        label[cls_idx] = 1
        return self.transform(image), label

    def read_labels(self, label_files):
        label_list = []
        for file in label_files:
            with open(file, "r") as f:
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
    img_size: int = 224,
    fill_color: Tuple[int, int, int] = (0, 0, 0),
    subset: str = "train",
    num_classes: int = 39,
    num_workers: int = 8,
    batch_size: int = 32,
    shuffle: bool = True,
    drop_last: bool = True,
):
    assert subset in ("train", "valid", "test")

    if subset == "train":
        augmentation = [
            Padding(fill=fill_color),
            Resize((img_size, img_size)),
            RandomHorizontalFlip(p=0.5),
            RandomRotation(degrees=(-20, 20)),
            ToTensor(),
        ]

    else:
        augmentation = [
            Padding(fill=fill_color),
            Resize((img_size, img_size)),
            ToTensor(),
        ]

    augmentation.append(
        Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    )

    augmentation = Compose(augmentation)

    data_loader = DataLoader(
        CustomDataset(
            path=path, subset=subset, transform=augmentation, num_classes=num_classes
        ),
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        drop_last=drop_last,
    )

    return data_loader
