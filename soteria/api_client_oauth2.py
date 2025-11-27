import asyncio
import os
import time
from typing import Optional, Dict
from soteria.api_client import ApiClient
from soteria.bearer_token_auth import BearerTokenAuth
from soteria.api_error import ApiError
from dotenv import load_dotenv

load_dotenv(verbose=True)

class ApiClientOAuth2:
    def __init__(self, base_url, token_url,
                 client_id: Optional[str]=None, client_secret: Optional[str]=None, scope: Optional[str]=None):
        self.token: str | None = None
        self.expires_at: float = 0
        self.base_url = base_url
        self.token_url = token_url
        self.client_id = os.getenv('SOTERIA_CLIENT_ID', client_id)
        self.client_secret = os.getenv('SOTERIA_CLIENT_SECRET', client_secret)
        self.scope = scope or os.getenv('SOTERIA_CLIENT_SCOPE', None)
        self.oauth2_client = ApiClient(base_url=self.base_url)

    async def authenticate(self) -> str:
        auth_form = {"client_id": self.client_id, "client_secret": self.client_secret,
                     "grant_type": "client_credentials"}
        response = await self.oauth2_client.post(self.token_url, data=auth_form)
        token = response.json().get('access_token')
        expires_in = response.json().get('expires_in', 1800)
        scope = response.json().get('scope')
        if not token:
            raise ApiError("OAuth2 Authentication failed", body=str(response))
        self.token = token
        self.expires_at = time.time() + expires_in
        self.scope = scope
        self.oauth2_client = ApiClient(base_url=self.base_url, auth=BearerTokenAuth(token=self.token), max_retries=2,)
        return token

    async def _is_expired(self) -> bool:
        return not self.token or time.time() >= self.expires_at

    async def ensure_token(self):
        if self._is_expired():
            await self.refresh()
            # raise ApiError("OAuth2 Token Expired - recall authenticate()")

    async def refresh(self):
        self.token = await self.authenticate()

    async def http_get(self, path, params:Optional[Dict[str, str]]=None, headers:Optional[Dict[str, str]]=None):
        await self.ensure_token()
        return await self.oauth2_client.get(path, params=params, headers=headers)

    async def http_post(self, path, body, headers:Optional[Dict[str, str]]=None):
        await self.ensure_token()
        return await self.oauth2_client.post(path, body=body, headers=headers)

    async def http_put(self, path, body, headers:Optional[Dict[str, str]]=None):
        await self.ensure_token()
        return await self.oauth2_client.put(path, body=body, headers=headers)

    async def http_delete(self, path):
        await self.ensure_token()
        return await self.oauth2_client.delete(path)

    async def http_patch(self, path, body):
        await self.ensure_token()
        return await self.oauth2_client.patch(path, body=body)

    async def http_options(self, path):
        await self.ensure_token()
        return await self.oauth2_client.request("OPTIONS", path)

    async def http_head(self, path):
        await self.ensure_token()
        return await self.oauth2_client.request("HEAD", path)

    async def close(self) -> None:
        await self.oauth2_client.aclose()