import argparse
import requests
import numpy as np
from PIL import Image
from io import BytesIO
from typing import *

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms

from dataset import Padding
from quantize import ptq_serving, qat_serving


class_info = {
    # foods
    '소고기': 0, '치킨': 1, '닭발': 2, '닭갈비': 3, '마른 안주': 4,
    '두부 김치': 5, '황도': 6, '계란말이': 7, '어묵탕': 8, '감자 튀김': 9, 
    '곱창': 10, '화채': 11, '짬뽕': 12, '짜파게티': 13, '라면': 14, 
    '양꼬치': 15, '나초': 16, '나가사키 짬뽕': 17, '피자': 18, '삼겹살': 19, 
    '족발': 20, '육회': 21, '연어': 22, '회': 23, '새우튀김': 24,
    
    # drinks
    '맥주': 25, '카스': 26, '참이슬 후레쉬': 27, '참이슬 오리지널': 28,
    '처음처럼': 29, '하이볼': 30, '하이트': 31, '진로': 32, '켈리': 33, 
    '클라우드': 34, 'OB': 35, '새로': 36, '소주': 37, '테라': 38,
}

class_info_rev = {v: k for k, v in class_info.items()}


transformation = transforms.Compose([
    Padding(fill=(0, 0, 0)),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
])


def load_image(img_url: str):
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content)).convert('RGB')
    img = transformation(img)
    img = img.unsqueeze(dim=0)
    return img, img_url


def inference(src: torch.Tensor, model: nn.Module, threshold: int=0.5):
    model.eval()
    result_list = []
    with torch.no_grad():
        outputs = model(src)
        result = outputs[0].detach().numpy()
        indices = np.where(result > threshold)[0]
        for idx in indices:
            result_list.append(class_info_rev[int(idx)])
    return result_list


def load_model(model_name: str, weight: str, num_classes: int, quantization: str='none'):
    q = True if quantization != 'none' else False

    # load model
    if model_name == 'shufflenet':
        from models.shufflenet import ShuffleNetV2
        model = ShuffleNetV2(num_classes=num_classes, pre_trained=False, quantize=q)
        
    elif model_name == 'resnet18':
        from models.resnet import resnet18
        model = resnet18(num_classes=num_classes, pre_trained=False, quantize=q)
        
    elif model_name == 'resnet50':
        from models.resnet import resnet50
        model = resnet50(num_classes=num_classes, pre_trained=False, quantize=q)
        
    else:
        raise ValueError(f'model name {model_name} does not exists.')
    
    # quantization
    if quantization == 'ptq':
        model = ptq_serving(model=model, weight=weight)

    elif quantization == 'qat':
        model = qat_serving(model=model, weight=weight)

    else: # 'none'
        pass

    return model


def classify(
    img_url: str, 
    model_name: str, 
    weight: str, 
    threshold: float=0.5, 
    quantization: str='none',
    num_classes: int=39,
) -> List[str]: 
    q = True if quantization != 'none' else False

    # load model
    model = load_model(model_name=model_name, weight=weight, num_classes=39, quantization=quantization)

    # load image
    img, img_url = load_image(img_url=img_url)

    # inference
    result = inference(img, model, threshold)

    return result