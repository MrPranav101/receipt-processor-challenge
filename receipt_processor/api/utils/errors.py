from fastapi.responses import JSONResponse


def in_between(min_inclusive: int, max_exclusive: int, status_code: int) -> bool:
    return min_inclusive <= status_code < max_exclusive


def user_error(
        status_code: int = 400,
        message: str = None,
        payload: any = None,
        headers: dict = None,
) -> JSONResponse:
    if not in_between(400, 500, status_code):
        raise ValueError(
            f"Invalid status code {status_code} for user error "
            f"response must be between 400 and 500")
    response_body = {}
    if message:
        response_body["message"] = message
    if payload:
        response_body["payload"] = payload
    return JSONResponse(
        status_code=status_code,
        content=response_body,
        headers=headers,
    )


def server_error(
        status_code: int = 500,
        message: str = None,
        payload: any = None,
        headers: dict = None,
) -> JSONResponse:
    if not in_between(500, 600, status_code):
        raise ValueError(
            f"Invalid status code {status_code} for user error "
            f"response must be between 500 and 600")
    response_body = {}
    if message:
        response_body["message"] = message
    if payload:
        response_body["payload"] = payload
    return JSONResponse(
        status_code=status_code,
        content=response_body,
        headers=headers,
    )
