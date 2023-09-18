
from fastapi import FastAPI

from receipt_processor.api.middleware.context import ContextMiddleware
from receipt_processor.config import (
    APP_NAME,
    LOG_LEVEL,
    VERSION,
    OPENAPI_VERSION
)
from receipt_processor.logger import get_logger


# initialize FastAPI instance
app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    description='A simple API to process receipts',
    openapi_version=OPENAPI_VERSION,
)

logger = get_logger(
    name=APP_NAME,
    log_level=LOG_LEVEL
)

app.add_middleware(ContextMiddleware)
