from datetime import datetime

import peewee

from api.config.exceptions import NotFoundException
from core.config.orm_config import db
from core.config.var_config import DB_SCHEMA


class BaseEntity(peewee.Model):
    class Meta:
        database = db
        schema = DB_SCHEMA

    id = peewee.AutoField(primary_key=True)
    created_at = peewee.DateTimeField(
        default=datetime.now,
    )
    updated_at = peewee.DateTimeField(
        default=datetime.now,
    )
    is_deleted = peewee.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def rollback_delete(self):
        self.is_deleted = False
        self.save()

    @classmethod
    def get_or_raise(cls, entity_id: int) -> "BaseEntity":
        entity = cls.get_or_none(entity_id)
        if entity is None or entity.is_deleted is True:
            raise NotFoundException(target_entity=cls, target_id=entity_id)
        return entity
