import traceback
from asyncio import create_task
from datetime import datetime

from fastapi import status, Request, HTTPException
from fastapi.responses import JSONResponse
from peewee import DoesNotExist

from api.config.exceptions import ForbiddenException
from app import app
from core.util.logger import logger
from core.util.slack import send_slack_message


@app.exception_handler(HTTPException)
async def handle_bad_request_exception(request: Request, exc: HTTPException):
    trace_info = traceback.format_exc()

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": f"{exc.__class__.__name__}",
            "message": exc.detail,
            "metadata": {
                "request_info": {"url": str(request.url), "method": request.method},
                "request_headers": {
                    header[0]: header[1] for header in request.headers.items()
                },
            },
        },
    )


@app.exception_handler(Exception)
async def handle_unexpected_exceptions(
    request: Request, exc: Exception
) -> JSONResponse:
    trace_info = traceback.format_exc()

    error_message = f"{datetime.now()} [{exc.__class__.__name__}] unexpected error occurred :: message - {str(exc)} trace_info - {trace_info}"
    logger.error(error_message)
    create_task(
        send_slack_message(
            channel="#error-logs",
            icon_emoji=":collision:",
            sender_name="님들오류남빨리안고치면인생망함",
            message=error_message + "<!channel>",
        )
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": f"{exc.__class__.__name__}", "message": str(exc)},
    )


@app.exception_handler(DoesNotExist)
async def handle_peewee_not_found_exception(exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": f"{exc.__class__.__name__}",
            "message": "not found entity for id",
        },
    )


@app.exception_handler(ForbiddenException)
async def handle_forbidden_exception(exc: ForbiddenException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": f"{exc.__class__.__name__}", "message": exc.detail},
    )
