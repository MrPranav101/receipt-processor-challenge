import os
import redis

from fastapi import Request
from fastapi.responses import JSONResponse

from receipt_processor.logger import get_logger
from receipt_processor.api.routers import main
from receipt_processor.api import app

app.include_router(main.router)


@app.on_event("startup")
async def startup():
    app.state.logger = get_logger(
        name='receipt-processor',
        log_level='DEBUG'
    )
    try:
        pass
    except Exception as e:
        app.state.logger.error(f"Failed to establish redis connection pool || Error: {e}")
        app.state.redis_pool = None


@app.api_route("/{path_name:path}", include_in_schema=True)
async def catch_all(request: Request, path_name: str) -> JSONResponse:
    return JSONResponse(
        content={
            "description": "Details not found",
            "request_method": request.method,
            "path_name": path_name
        },
        status_code=404
    )


@app.on_event("shutdown")
async def shutdown():
    app.state.logger.info(f"Shutting Down {APP_NAME}.")
    try:
        pass
    except Exception as e:
        app.state.logger.error(f"Failed to close a connection on shutdown || Error: {e}")
