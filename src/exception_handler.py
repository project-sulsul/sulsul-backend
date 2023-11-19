import traceback
from fastapi import status, Request
from fastapi.responses import JSONResponse

from app import app


@app.exception_handler(Exception)
async def hanlde_exceptions(request: Request, exc):
    trace_info = traceback.format_exc()

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": f"{exc.__class__.__name__}",
            "message": str(exc),
            "trace_info": trace_info
        }
    )
