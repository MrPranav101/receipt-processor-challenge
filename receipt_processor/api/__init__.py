import os

from fastapi import FastAPI, Depends

from receipt_processor.api.middleware.context import ContextMiddleware


# initialize FastAPI instance
app = FastAPI(
    title='Receipt Processor API',
    version='0.0.1'
)

app.add_middleware(ContextMiddleware)
app.router.responses = {404: {"description": "Not found"}}
