from uuid import uuid4
from fastapi import Header


def optional_headers(
    request_id: str = Header(default=str(uuid4()), alias="x-request-id", example=str(uuid4()))
):
    """Function to put in routers for required logging ids

    Args:
        request_id (str, optional): Request ID for logging. Defaults to Header(default=str(uuid4()), alias="x-request-id", example=str(uuid4()))
    """
    return
