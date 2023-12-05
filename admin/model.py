import peewee
from pydantic import BaseModel

from core.config.orm_config import db
from core.config.var_config import DB_SCHEMA


class Admin(peewee.Model):
    id = peewee.AutoField(primary_key=True)
    username = peewee.CharField()
    password = peewee.CharField()

    class Meta:
        table_name = "admin"
        database = db
        schema = DB_SCHEMA


class AdminSigninModel(BaseModel):
    username: str
    password: str
