import os, inspect, importlib
from peewee import Model

from app_config import db


models = list()
def get_models(cdir: str = None):
    for dirname in os.listdir(cdir):
        if len(dirname.split(".")) == 1 and dirname not in ("LICENSE", "Procfile", "runserver", "zip", "venv"):
            get_models(f"{cdir + '/' if cdir else ''}{dirname}")
        else:
            if dirname == "model.py":
                model_module = ".".join(f"{cdir}/{dirname}".split(".")[0].split("/"))
                model = importlib.import_module(model_module)
                global models
                models.extend(
                    [ obj for _, obj in inspect.getmembers(model) if inspect.isclass(obj) and issubclass(obj, Model) and obj is not Model ]
                )
get_models("v1")

with db.atomic():
    print(models)
