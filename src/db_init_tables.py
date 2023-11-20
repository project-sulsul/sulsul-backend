import os, inspect, importlib
from peewee import Model
from playhouse import signals

from src.orm import db


models = list()
def get_models(version: str = "v1", model_filename: str = "model.py"):
    for dirname in os.listdir(version):
        if len(dirname.split(".")) == 1:
            get_models(f"{version + '/' if version else ''}{dirname}", model_filename)
        else:
            if dirname == model_filename:
                model_module = ".".join(f"{version}/{dirname}".split(".")[0].split("/"))
                model = importlib.import_module(model_module)
                global models
                models.extend(
                    [ obj for _, obj in inspect.getmembers(model) if inspect.isclass(obj) and issubclass(obj, Model) and obj is not Model and obj is not signals.Model ]
                )

get_models("v1", "model.py")

db.connect()

from admin.model import Admin
db.create_tables([Admin], safe=True)

db.drop_tables(models)
db.create_tables(models, safe=True)

from v1.pairing.model import Pairing
data = [
    {"type": "술", "name": "소주", "image": None, "description": "소주예요"},
    {"type": "술", "name": "맥주", "image": None, "description": "맥주예요"},
    {"type": "술", "name": "하이볼", "image": None, "description": "하이볼이에요"},
    {"type": "술", "name": "막걸리", "image": None, "description": "막걸리예요"},
    {"type": "술", "name": "와인", "image": None, "description": "와인이에요"},
    {"type": "안주", "name": "패스트푸드", "image": None, "description": "패스트푸드예요"},
    {"type": "안주", "name": "육류", "image": None, "description": "육류예요"},
    {"type": "안주", "name": "탕류", "image": None, "description": "탕류예요"},
    {"type": "안주", "name": "튀김류", "image": None, "description": "튀김류예요"},
    {"type": "안주", "name": "과일", "image": None, "description": "과일이에요"},
    {"type": "안주", "name": "과자", "image": None, "description": "과자예요"},
    {"type": "안주", "name": "면류", "image": None, "description": "면류예요"},
    {"type": "안주", "name": "회", "image": None, "description": "회예요"},
    {"type": "안주", "name": "마른안주", "image": None, "description": "마른안주예요"},
]
for record in data:
    Pairing.create(
        type=record["type"],
        name=record["name"],
        image=record["image"],
        description=record["description"],
    )

# from v1.user.model import User
# user = User.create(
#     uid="test_user_uid",
#     social_type="google",
# )

db.close()
