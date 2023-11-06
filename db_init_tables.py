import os, inspect, importlib, logging
from peewee import Model

from src.orm import db


models = list()
def get_models(cdir: str = None, model_filename: str = "model.py"):
    for dirname in os.listdir(cdir):
        if len(dirname.split(".")) == 1:
            get_models(f"{cdir + '/' if cdir else ''}{dirname}", model_filename)
        else:
            if dirname == model_filename:
                model_module = ".".join(f"{cdir}/{dirname}".split(".")[0].split("/"))
                model = importlib.import_module(model_module)
                global models
                models.extend(
                    [ obj for _, obj in inspect.getmembers(model) if inspect.isclass(obj) and issubclass(obj, Model) and obj is not Model ]
                )

get_models("v1", "model.py")

db.connect()
db.create_tables(models, safe=True)
db.close()
