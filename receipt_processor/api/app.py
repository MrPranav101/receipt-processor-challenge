from fastapi import Request
from fastapi.responses import JSONResponse

from receipt_processor.config import APP_NAME
from receipt_processor.api.routers import receipts
from receipt_processor.api import app, logger

app.include_router(receipts.router)


@app.on_event("startup")
async def startup():
    app.state.logger = logger
    try:
        pass
    except Exception as e:
        app.state.logger.error(f"Failed to establish redis connection pool || Error: {e}")


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
