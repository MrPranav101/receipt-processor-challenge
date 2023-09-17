from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi


from receipt_processor.config import APP_NAME
from receipt_processor.api.routers import receipts
from receipt_processor.api import app, logger
from receipt_processor.db import init_db
from receipt_processor.api.utils.errors import user_error

app.include_router(receipts.router)


@app.on_event("startup")
async def startup():
    app.state.logger = logger
    app.state.logger.info(f"Starting {APP_NAME}.")
    try:
        await init_db()
    except Exception as e:
        app.state.logger.error(f"Failed to establish sql connection pool || Error: {e}")


@app.on_event("shutdown")
async def shutdown():
    app.state.logger.info(f"Shutting Down {APP_NAME}.")
    try:
        pass
    except Exception as e:
        app.state.logger.error(f"Failed to close a connection on shutdown || Error: {e}")


@app.exception_handler(RequestValidationError)
async def standard_validation_exception_handler(request: Request, exc: RequestValidationError):
    return user_error(
        status_code=400,
        message=jsonable_encoder({"detail": exc.errors(), "body": exc.body})
    )


def custom_openapi():
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            routes=app.routes,
            tags=app.openapi_tags,
            servers=app.servers,
        )
        for _, method_item in app.openapi_schema.get('paths').items():
            for _, param in method_item.items():
                responses = param.get('responses')
                # remove 422 response, also can remove other status code
                if '422' in responses:
                    del responses['422']
    return app.openapi_schema


app.openapi = custom_openapi
