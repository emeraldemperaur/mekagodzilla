# Rate Limiter Middleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from collections import deque
import time


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit_per_min: int = 120, window_sec: int = 60):
        super().__init__(app)
        self.limit = limit_per_min
        self.window = float(window_sec)
        self.buckets:  dict[str, deque[float]] = {}

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        now = time.monotonic()
        dq = self.buckets.setdefault(client_ip, deque())
        while dq and now - dq[0] > self.window:
            dq.popleft()
        if len(dq) >= self.limit:
            return Response("WTF! Too Many HTTP Requests", 429)
        dq.append(now)
        return await call_next(request)
