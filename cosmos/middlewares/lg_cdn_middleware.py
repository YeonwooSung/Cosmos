"""Adds uuid to the request header for debugging."""

from uuid import uuid4
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

# custom modules
from cosmos.utils.logging import Logger
from cosmos.services.lg_bei_info import process_cdn_bei_info_cmd

logger = Logger()


class LgCdnBase64BodyMiddleware(BaseHTTPMiddleware):
    """Parse the base64 body of the requests for LG CDN testing.

    Args:
        app (fastapi.Request): Instance of a FastAPI class.
    """

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        """
        Implement the dispatch method.

        Args:
            request (fastapi.Request): Instance of a FastAPI class.
            call_next (function): Function to call next middleware.
        """

        try:
            url_str = str(request.url)
            if '/CdnCheckBEInfoCmd.cbec' in url_str:
                request_body = await request.body()
                request_id = request.state.request_id

                data = await process_cdn_bei_info_cmd(request_id, request_body.decode('utf-8'))
                return Response(content=data, status_code=200)

            response = await call_next(request)
            return response
        except Exception as e:
            logger.log_warning(
                f"method={request.method} | {request.url} | {request.state.request_id} | {e}"
            )
            return JSONResponse(status_code=500, content={"reason": str(e)})
