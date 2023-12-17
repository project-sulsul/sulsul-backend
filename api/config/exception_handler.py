import traceback

from fastapi import status, Request, HTTPException
from fastapi.responses import JSONResponse
from peewee import DoesNotExist

from app import app


@app.exception_handler(HTTPException)
async def handle_bad_request_exception(request: Request, exc: HTTPException):
    trace_info = traceback.format_exc()

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "metadata": {
                "request_info": {"url": str(request.url), "method": request.method},
                "request_headers": {
                    header[0]: header[1] for header in request.headers.items()
                },
            },
        },
    )


@app.exception_handler(Exception)
async def handle_exceptions(request: Request, exc: Exception) -> JSONResponse:
    trace_info = traceback.format_exc()

    # TODO 에러 보고

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": f"{exc.__class__.__name__}",
            "message": str(exc),
            "trace_info": trace_info,
        },
    )


@app.exception_handler(DoesNotExist)
async def handle_peewee_not_found_exception(
    request: Request, exc: Exception
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": f"{exc.__class__.__name__}",
            "message": "not found entity for id",
        },
    )
