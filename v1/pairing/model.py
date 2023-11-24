from typing import List
from datetime import datetime

import peewee
from playhouse.signals import Model, pre_save
from pydantic import BaseModel

from src.orm import db
from src.config.var_config import KST, DB_SCHEMA


class PairingCreateModel(BaseModel):
    type: str
    name: str
    image: str | None
    description: str | None


class PairingUpdateModel(BaseModel):
    type: str
    name: str
    image: str | None
    description: str | None
    is_deleted: bool


class PairingResponseModel(BaseModel):
    id: int
    type: str
    name: str
    image: str | None
    description: str | None


class PairingAdminResponseModel(BaseModel):
    id: int
    type: str
    name: str
    image: str | None
    description: str | None
    created_at: str
    updated_at: str
    is_deleted: bool

class PairingListResponseModel(BaseModel):
    pairings: List[PairingResponseModel]


class Pairing(Model):
    id = peewee.AutoField(primary_key=True)
    type = peewee.CharField(max_length=10, null=False)
    name = peewee.CharField(max_length=100, null=False, unique=True)
    image = peewee.CharField(null=True)
    description = peewee.CharField(null=True)
    created_at = peewee.DateTimeField(default=datetime.now(KST).strftime("%Y-%m-%dT%H:%M:%S%z"))
    updated_at = peewee.DateTimeField(default=datetime.now(KST).strftime("%Y-%m-%dT%H:%M:%S%z"))
    is_deleted = peewee.BooleanField(default=False)

    class Meta:
        table_name = "pairing"
        database = db
        schema = DB_SCHEMA

    def dto(self) -> PairingResponseModel:
        return PairingResponseModel(
            id=self.id,
            type=self.type,
            name=self.name,
            image=self.image,
            description=self.description,
        )
    
    def dto_admin(self) -> PairingAdminResponseModel:
        return PairingAdminResponseModel(
            id=self.id,
            type=self.type,
            name=self.name,
            image=self.image,
            description=self.description,
            created_at=self.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
            updated_at=self.updated_at.strftime("%Y-%m-%dT%H:%M:%S"),
            is_deleted=self.is_deleted,
        )


@pre_save(sender=Pairing)
def pre_save(model_class, instance: Pairing, created):
    if not created:
        instance.updated_at = datetime.now(KST).strftime("%Y-%m-%dT%H:%M:%S%z")
