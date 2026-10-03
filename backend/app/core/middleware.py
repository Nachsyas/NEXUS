from collections.abc import Awaitable, Callable

import uuid6
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware to propagate or generate unique X-Request-ID header per request."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        incoming_request_id = request.headers.get("X-Request-ID")
        request_id = incoming_request_id if incoming_request_id else str(uuid6.uuid7())

        # Store in request state for downstream handlers
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
