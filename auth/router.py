from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse, RedirectResponse

from google.oauth2 import id_token
from google.auth.transport import requests

from .model import GoogleCredentialsModel
from .secrets import *


auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication", "Google"],
)


@auth_router.post("/sign-in/google")
async def sign_in_with_google(
    request: Request,
    response: Response,
    google_credentials: GoogleCredentialsModel
):
    try:
        id_info = id_token.verify_oauth2_token(
            google_credentials.model_dump()["credential"], requests.Request(), 
            GOOGLE_CLIENT_ID,
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": f"{e.__class__.__module__}.{e.__class__.__name__}",
                "error_type": "OAuth_Exception",
                "message": str(e),
            }
        )
