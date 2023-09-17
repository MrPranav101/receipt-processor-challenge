
from fastapi import FastAPI

from receipt_processor.api.middleware.context import ContextMiddleware
from receipt_processor.config import APP_NAME, LOG_LEVEL
from receipt_processor.logger import get_logger


# initialize FastAPI instance
app = FastAPI(
    title='Receipt Processor API',
    version='0.0.1'
)

logger = get_logger(
        name=APP_NAME,
        log_level=LOG_LEVEL
    )

app.add_middleware(ContextMiddleware, logger=logger)
app.router.responses = {404: {"description": "Not found"}}
