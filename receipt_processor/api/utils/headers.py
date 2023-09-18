from uuid import uuid4
from fastapi import Header


def optional_headers(
    request_id: str = Header(default=str(uuid4()), alias="x-request-id", examples=str(uuid4()))
):
    return
