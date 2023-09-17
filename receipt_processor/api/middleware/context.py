import logging
import time
from typing import Callable

from fastapi import Request, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp

from receipt_processor.logger import set_request_id


class ContextMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app: FastAPI,
            *,
            logger: logging.Logger
    ) -> None:
        self._logger = logger
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get('x-request-id')
        generate = False
        if not request_id:
            generate = True
        set_request_id(request_id, generate=generate)
        # process the request and get the response
        response = await call_next(request)
        return response


# class ContextMiddleware(BaseHTTPMiddleware):
#     def __init__(
#             self,
#             app: FastAPI,
#             *,
#             logger: logging.Logger
#     ) -> None:
#         self._logger = logger
#         super().__init__(app)

#     async def dispatch(self, request: Request, call_next):
#         request_id = request.headers.get('x-request-id')
#         generate = False
#         if not request_id:
#             generate = True
#         set_request_id(request_id, generate=generate)
#         # process the request and get the response
#         request_dict = await self._log_request(request)
#         self._logger.info(f"[Begin] [{request_dict['method']}] {request_dict['path']}", extra={"meta_data": {"request": request_dict}})
#         response, response_dict = await self._log_response(call_next,
#                                                            request)
#         self._logger.info(f"[End] [{request_dict['method']}] {request_dict['path']} [{response_dict['status']}]", extra={"meta_data": {"response": response_dict}})
#         return response

#     async def _log_request(
#         self,
#         request: Request
#     ) -> str:
#         """Logs request part
#             Arguments:
#            - request: Request

#         """

#         path = request.url.path
#         if request.query_params:
#             path += f"?{request.query_params}"

#         request_logging = {
#             "method": request.method,
#             "path": path,
#             "ip": request.client.host
#         }

#         return request_logging

#     async def _log_response(self,
#                             call_next: Callable,
#                             request: Request
#                             ) -> Response:
#         """Logs response part

#                Arguments:
#                - call_next: Callable (To execute the actual path function and get response back)
#                - request: Request
#                Returns:
#                - response: Response
#                - response_logging: str
#         """

#         start_time = time.perf_counter()
#         response = await self._execute_request(call_next, request)
#         finish_time = time.perf_counter()

#         overall_status = "successful" if response.status_code < 400 else "failed"
#         execution_time = finish_time - start_time

#         response_logging = {
#             "status": overall_status,
#             "status_code": response.status_code,
#             "time_taken": f"{execution_time:0.4f}s"
#         }

#         return response, response_logging

#     async def _execute_request(self,
#                                call_next: Callable,
#                                request: Request
#                                ) -> Response:
#         """Executes the actual path function using call_next.
#                It also injects "X-API-Request-ID" header to the response.

#                Arguments:
#                - call_next: Callable (To execute the actual path function
#                             and get response back)
#                - request: Request
#                Returns:
#                - response: Response
#         """
#         try:
#             response: Response = await call_next(request)
#             return response

#         except Exception as e:
#             self._logger.exception(
#                 extra={
#                     "meta_data": {
#                         "path": request.url.path,
#                         "method": request.method,
#                         "reason": e
#                     }
#                 }
#             )
