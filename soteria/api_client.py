from typing import Any, Dict, Optional, Tuple, Union, Sequence, TypeVar
from pydantic import BaseModel
import httpx
import asyncio
from soteria.auth_strategy import AuthStrategy
from soteria.api_error import ApiError
from soteria.hmac_auth import HMACAuth
import time
import random
import json as pyjson
from urllib.parse import urlencode

# Api Client
T = TypeVar('T', bound=BaseModel)
class ApiClient:
    """
      Asynchronous Soteria API Client
      - Injectable AuthStrategy
      - Strategies: ApiKey, Bearer Token, OAuth2ClientCredentials, HMAC Authentication
      - Retries w/ exponential backoff
      - Optional QPS functionality (client-wide rate limiting)
      """
    def __init__(self, base_url: str, auth: Optional[AuthStrategy] = None, *,
                 timeout: float = 15.0, max_retries: int = 3, backoff_factor: float = 0.5,
                 rate_limit_per_sec: Optional[float] = None, default_headers: Optional[Dict[str, str]] = None,
                 default_params: Optional[Dict[str, Any]] = None) -> None:
        self.base_url = base_url.rstrip('/')
        self.auth = auth
        self.timeout = timeout
        self.max_retries = max(0, max_retries)
        self.backoff_factor = max(0.0, backoff_factor)
        self.default_headers = default_headers or {}
        self.default_params = default_params or {}
        self._client = httpx.AsyncClient = httpx.AsyncClient(timeout= timeout, base_url=self.base_url)
        self._rate_lock = asyncio.Lock()
        self._min_interval = (1.0 / rate_limit_per_sec) if rate_limit_per_sec and rate_limit_per_sec > 0 else 0.0
        self._last_at = 0.0

    async def aclose(self) -> None:
        await self._client.aclose()

    # Client Utility Methods
    def _merge_headers(self, headers: Optional[Dict[str, str]]) -> Dict[str, str]:
        merged = dict(self.default_headers)
        if headers:
            merged.update(headers)
        return merged

    def _merge_params(self, params: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        merged = dict(self.default_params)
        if params:
            merged.update(params)
        return merged

    async def _respect_rate_limit(self) -> None:
        if self._min_interval <= 0:
            return
        async with self._rate_lock:
            now = time.perf_counter()
            elapsed = now - self._last_at
            if elapsed < self._min_interval:
                await asyncio.sleep(self._min_interval - elapsed)
            self._last_at = time.perf_counter()

    @staticmethod
    def _is_transient(status_code: int) -> bool:
        return status_code in (429, 500, 502, 503, 504)

    async def _send_with_retries(self, _request: httpx.Request) -> httpx.Response:
        attempt = 0
        while True:
            try:
                await self._respect_rate_limit()
                response: httpx.Response = await self._client.send(_request, stream=False)
                if response.status_code in (429, 500, 502, 503, 504) and attempt < self.max_retries:
                    await self._backoff_sleep(attempt)
                    attempt += 1
                    continue
                return response
            except (httpx.ConnectError, httpx.ReadTimeout, httpx.WriteError, httpx.RemoteProtocolError) as e:
                if attempt < self.max_retries:
                    await self._backoff_sleep(attempt)
                    attempt += 1
                    continue
                raise ApiError(message=F"Network error: {e}", status_code=429) from e
        raise AssertionError("unreachable")


    async def _backoff_sleep(self, attempt: int) -> None:
        # Exponential backoff with jitter
        delay = self.backoff_factor * (2 ** attempt)
        jitter = 0.5 + random.random() * 0.5 # 0.5 - 1.0
        await asyncio.sleep(delay * jitter)

    # Public HTTP Helpers
    async def request(self, method: str, path: str, *,
                      params: Optional[Dict[str, Any]] = None, json: Optional[Any] = None,
                      data: Optional[Union[Dict[str,Any]],
                      Sequence[Tuple[str,Any]], bytes, bytearray, str] = None,
                      headers: Optional[Dict[str, str]] = None) -> Any:
        url_path = "/" + path.lstrip('/')
        final_params = self._merge_params(params)
        final_headers = self._merge_headers(headers)
        body_bytes: bytes
        # Body Handling
        if json is not None:
            body_bytes = pyjson.dumps(json, separators=(',', ':')).encode("utf-8")
            final_headers.setdefault('Content-Type', 'application/json')
        elif data is not None:
            if isinstance(data, (bytes, bytearray)):
                body_bytes = bytes(data)
            elif isinstance(data, str):
                body_bytes = data.encode("utf-8")
            else:
                # form-encode fallback
                body_bytes = urlencode(data, doseq=True).encode("utf-8")
                final_headers.setdefault('Content-Type', 'application/x-www-form-urlencoded')
        else:
            body_bytes = b""

        if isinstance(self.auth, HMACAuth):
            # noinspection PyProtectedMember
            body_sha = HMACAuth._sha256_b64(body_bytes)
            query_str = str(httpx.QueryParams(final_params)) if final_params else ""
            full_path = f"{url_path}?{query_str}" if query_str else url_path
            final_headers[":_method"] = method.upper()
            final_headers[":_path"] = full_path
            final_headers["_body_sha256"] = body_sha

        if self.auth:
            await self.auth.attach(final_headers)

        request = self._client.build_request(method=method.upper(), url=url_path, params=final_params,
                                             headers=final_headers, content=body_bytes,)
        response = await self._send_with_retries(request)
        if 200 <= response.status_code < 300:
            ctype = response.headers.get("Content-Type", "")
            if "application/json" in ctype:
                try:
                    return response.json()
                except Exception:
                    return response.text
            return response.text if "text/" in ctype else response.content
        raise ApiError(message=F"Request failed: {method} {url_path}",
                       status_code=response.status_code, body=response.text)

    # HTTP Method Helpers
    async def get(self, path: str, **kwargs: Any) -> Any:
        return await self.request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs: Any) -> Any:
        return await self.request("POST", path, **kwargs)

    async def put(self, path: str, **kwargs: Any) -> Any:
        return await self.request("PUT", path, **kwargs)

    async def patch(self, path: str, **kwargs: Any) -> Any:
        return await self.request("PATCH", path, **kwargs)

    async def delete(self, path: str, **kwargs: Any) -> Any:
        return await self.request("DELETE", path, **kwargs)

    async def head(self, path: str, **kwargs: Any) -> Any:
        return await self.request("HEAD", path, **kwargs)

    async def options(self, path: str, **kwargs: Any) -> Any:
        return await self.request("OPTIONS", path, **kwargs)

    async def trace(self, path: str, **kwargs: Any) -> Any:
        return await self.request("TRACE", path, **kwargs)

