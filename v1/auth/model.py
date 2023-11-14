from pydantic import BaseModel


class GoogleCredentialsModel(BaseModel):
    id_token: str
