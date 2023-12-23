from io import BytesIO
from typing import *

import numpy as np
import requests
from PIL import Image
from pydantic import BaseModel

from ai.dataset import Padding
from ai.quantize import ptq_serving, qat_serving
from torch import no_grad, Tensor
from torch.nn import Module
from torchvision.transforms import Compose, Resize, ToTensor, Normalize

class_info = {
    # foods
    "소고기": 0,
    "치킨": 1,
    "닭발": 2,
    "닭갈비": 3,
    "마른 안주": 4,
    "두부 김치": 5,
    "황도": 6,
    "계란말이": 7,
    "어묵탕": 8,
    "감자 튀김": 9,
    "곱창": 10,
    "화채": 11,
    "짬뽕": 12,
    "짜파게티": 13,
    "라면": 14,
    "양꼬치": 15,
    "나초": 16,
    "나가사키 짬뽕": 17,
    "피자": 18,
    "삼겹살": 19,
    "족발": 20,
    "육회": 21,
    "연어": 22,
    "회": 23,
    "새우튀김": 24,
    # drinks
    "맥주": 25,
    "카스": 26,
    "참이슬 후레쉬": 27,
    "참이슬 오리지널": 28,
    "처음처럼": 29,
    "하이볼": 30,
    "하이트": 31,
    "진로": 32,
    "켈리": 33,
    "클라우드": 34,
    "OB": 35,
    "새로": 36,
    "소주": 37,
    "테라": 38,
}

class_info_rev = {v: k for k, v in class_info.items()}

transformation = Compose(
    [
        Padding(fill=(0, 0, 0)),
        Resize((224, 224)),
        ToTensor(),
        Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ]
)


def load_image(img_url: str):
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content)).convert("RGB")
    img = transformation(img)
    img = img.unsqueeze(dim=0)
    return img, img_url


def inference(src: Tensor, model: Module, threshold: float = 0.5) -> Dict:
    model.eval()
    result_list = {"foods": [], "alcohols": []}
    with no_grad():
        outputs = model(src)
        result = outputs[0].detach().numpy()
        indices = np.where(result > threshold)[0]

        food_indices = indices[indices <= 24]
        alcohol_indices = indices[indices > 24]

        result_list["foods"] = [class_info_rev[idx] for idx in food_indices]
        result_list["alcohols"] = [class_info_rev[idx] for idx in alcohol_indices]

    return result_list


def load_model(
    model_name: str, weight: str, num_classes: int, quantization: str = "qat"
):
    q = True if quantization != "none" else False

    # load model
    if model_name == "resnet18":
        from ai.models.resnet import custom_resnet18

        model = custom_resnet18(num_classes=num_classes, pre_trained=False, quantize=q)

    elif model_name == "resnet50":
        from ai.models.resnet import custom_resnet50

        model = custom_resnet50(num_classes=num_classes, pre_trained=False, quantize=q)

    else:
        raise ValueError(f"model name {model_name} does not exists.")

    # quantization
    if quantization == "ptq":
        model = ptq_serving(model=model, weight=weight)

    elif quantization == "qat":
        model = qat_serving(model=model, weight=weight)

    else:  # 'none'
        pass

    return model


class ClassificationResultDto(BaseModel):
    foods: List[str]
    alcohols: List[str]


def classify(
    img_url: str,
    weight_file_path: str,
    model_name: str = "resnet18",
    threshold: float = 0.5,
    quantization: str = "qat",
    num_classes: int = 39,
) -> ClassificationResultDto:
    # load model
    model = load_model(
        model_name=model_name,
        weight=weight_file_path,
        num_classes=num_classes,
        quantization=quantization,
    )

    # load image
    img, img_url = load_image(img_url=img_url)

    # inference
    result = inference(img, model, threshold)

    return ClassificationResultDto(foods=result["foods"], alcohols=result["alcohols"])
