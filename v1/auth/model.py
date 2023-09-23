from pydantic import BaseModel


class GoogleCredentialsModel(BaseModel):
    clientId: str | None
    client_id: str | None
    credential: str
    select_by: str | None
