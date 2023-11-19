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

# db.drop_tables(models)
db.create_tables(models, safe=True)

# from v1.user.model import User
# user = User.create(
#     uid="test_user_uid",
#     social_type="google",
# )

db.close()
