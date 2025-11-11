# Trulioo API Interface Interactions
from __future__ import annotations

import random
from urllib.parse import urlencode

from pydantic import BaseModel

from artificer import ASCI_BLUE, ASCI_RESET, ASCI_ARROW
from artisan import Artisan
import asyncio
import base64
import hashlib
import hmac
import json as pyjson
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional, Protocol, Tuple, Union, Sequence, TypeVar
import httpx

class Soteria:
    _instance = None
    """
    Asynchronous Soteria API Client
    - Injectable AuthStrategy
    - Strategies: ApiKey, Bearer Token, OAuth2ClientCredentials, HMAC Authentication
    - Retries w/ exponential backoff
    - Optional QPS functionality (client-wide rate limiting)
    """

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If no instance exists, create a new one using the parent's __new__
            cls._instance = super(Soteria, cls).__new__(cls)
        return cls._instance  # Always return the existing instance

    def __init__(self, heimdall):
        if not hasattr(self, '_initialized'):
            self.artisan = Artisan()
            self.heimdall = heimdall
            self._initialized = True
            self.heimdall.info_log(F"Initialized Soteria T-NAPI Interface::{self.artisan.userid}@trulioo.com")
            print(F"{ASCI_BLUE}{ASCI_ARROW} Soteria Initialized{ASCI_RESET}")

    def api_client_init(self, base_url: str, auth: Optional[AuthStrategy] = None, *,
                        timeout: float = 15.0, max_retries: int = 3, backoff_factor: float = 0.5,
                        rate_limit_per_sec: Optional[float] = None, default_headers: Optional[Dict[str, str]] = None,
                        default_params: Optional[Dict[str, Any]] = None) -> None:
        pass

# Api Client
T = TypeVar('T', bound=BaseModel)
class ApiClient:
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


# Errors
class ApiError(Exception):
    def __init__(self, message: str, * , status_code:Optional[int]=None, body:Optional[str]=None):
        super().__init__(message)
        self.status_code = status_code
        self.body = body

    def __str__(self) -> str:
        base = super().__str__()
        if self.status_code is not None:
            base += f" (status code={self.status_code})"
        if self.body:
                base += f" body={self.body[:400]}"
        return base

# Authentication
## Authentication Strategy Protocol
class AuthStrategy(Protocol):
    async def attach(self, request_headers: Dict[str, str]) -> None:
        """
        Mutates request_headers to add whatever authentication protocol is needed for auth.
        Called on every request
        """
        ...

## Authentication Strategies
@dataclass
class ApiKeyAuth(AuthStrategy):
    key: str
    header_name: str = "X-API-Key"
    in_query: bool = False

    async def attach(self, request_headers: Dict[str, str]) -> None:
        if not self.in_query:
            request_headers[self.header_name] = self.key

@dataclass
class BearerTokenAuth(AuthStrategy):
    token: str

    async def attach(self, request_headers: Dict[str, str]) -> None:
        request_headers["Authorization"] = f"Bearer {self.token}"

class OAuth2ClientCredentials(AuthStrategy):
    """
    Minimalistic OAuth2 client credentials flow with auto-refresh.
    """
    def __init__(self, token_url: str, client_id: str, client_secret: str,
                 scope: Optional[str] = None, audience: Optional[str] = None,
                 timeout: float = 10.0,) -> None:
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.audience = audience
        self.timeout = timeout
        self._access_token: Optional[str] = None
        self._expires_at: float = 0.0
        self._lock = asyncio.Lock()

    async def _fetch_token(self) -> Tuple[str, float]:
        data = {"grant_type": "client_credentials"}
        if self.scope:
            data["scope"] = self.scope
        if self.audience:
            data["audience"] = self.audience
        auth = (self.client_id, self.client_secret)
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(self.token_url, data=data, auth=auth)
        if response.status_code != httpx.codes.OK:
            raise ApiError("OAuht2 token fetch failed", status_code=response.status_code, body=response.text)
        payload = response.json()
        token = payload["access_token"]
        expires_in = float(payload.get("expires_in", 3600))
        if not token:
            raise ApiError("OAuht2 response missing access_token", status_code=response.status_code, body=response.text)
        return token, time.time() + max(10.0, 0.9 * expires_in)

    async def _ensure_token(self) -> str:
        async with self._lock:
            now = time.time()
            if not self._access_token or now >= self._expires_at:
                token, exp = await self._fetch_token()
                self._access_token = token
                self._expires_at = exp
            return self._access_token

    async def attach(self, request_headers: Dict[str, str]) -> None:
        token = await self._ensure_token()
        request_headers["Authorization"] = f"Bearer {token}"

@dataclass
class HMACAuth(AuthStrategy):
    """
    Minimalistic HMAC authentication scheme:
    signature = base64(hmac_sha256(secret, f'{method}\n{path}\n{ts}\n{body_sha256}'))
    Header: Authorization: HMAC {key_id}: {signature};ts={ts}
    """
    key_id: str
    secret: str
    header_name: str = "Authorization"

    @staticmethod
    def _sha256_b64(data: bytes) -> str:
        return base64.b64encode(hashlib.sha256(data).digest()).decode("ascii")

    @staticmethod
    def _hmac_b64(secret: str, msg: str) -> str:
        digest = hmac.new(key=secret.encode(), msg=msg.encode("utf-8"), digestmod=hashlib.sha256).digest()
        return base64.b64encode(digest).decode("ascii")

    async def attach(self, request_headers: Dict[str, str]) -> None:
        # Client provides special pseudo-headers before sending:
        method = request_headers.pop(":_method", "GET")
        path = request_headers.pop(":_path", "/")
        body_hash = request_headers.pop(":_body_sha256", "")
        ts = str(int(time.time()))
        sig_payload = f"{method}\n{path}\n{ts}\n{body_hash}"
        sig = self._hmac_b64(self.secret, sig_payload)
        request_headers[self.header_name] = f"HMAC {self.key_id}:{sig};ts={ts}"

