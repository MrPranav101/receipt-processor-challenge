from fastapi import Request, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from receipt_processor.logger import set_request_id


class ContextMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app: FastAPI
    ) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get('x-request-id')
        generate = False
        if not request_id:
            generate = True
        set_request_id(request_id, generate=generate)
        response = await call_next(request)
        return response
