from soteria.auth_strategy import AuthStrategy
from soteria.api_error import ApiError
import asyncio
from typing import Optional, Tuple, Dict
import httpx
import time

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