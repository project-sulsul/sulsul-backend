from pydantic import BaseModel


class BaseDTO(BaseModel):

    @classmethod
    def from_orm(cls, entity):
        return cls(**entity.__data__)
