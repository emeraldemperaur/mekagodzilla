import asyncio
from typing import Optional, Dict
from soteria.api_client import ApiClient
from soteria.bearer_token_auth import BearerTokenAuth
from soteria.api_error import ApiError

class ApiClientTokenAuth(BearerTokenAuth):
    def __init__(self, base_url: str, token:Optional[str]=None):
        self.base_url = base_url
        self.token: str | None = token
        self.token_client = ApiClient(base_url=base_url, auth=BearerTokenAuth(token=token), max_retries=2,)

    async def authenticate_json(self, auth_path, login_body):
        response = await self.token_client.post(path=auth_path, json=login_body)
        token = response.get("access_token")
        if not token:
            raise ApiError("Authentication failed: token not found", body=str(response))
        self.token = token
        self.token_client = ApiClient(base_url=self.base_url, auth=BearerTokenAuth(token=self.token), max_retries=2,)
        return token

    async def authenticate_form(self, auth_path, login_body) -> str:
        response = await self.token_client.post(path=auth_path, data=login_body)
        token = response.get("access_token")
        if not token:
            raise ApiError("Authentication failed: token not found", body=str(response))
        self.token = token
        self.token_client = ApiClient(base_url=self.base_url, auth=BearerTokenAuth(token=self.token), max_retries=2,)
        return token


    async def http_get(self, path, params:Optional[Dict[str, str]]=None):
        return await self.token_client.get(path, params=params)

    async def http_post_json(self, path, body):
        return await self.token_client.post(path, json=body)

    async def http_post_form(self, path, body):
        return await self.token_client.post(path, data=body)

    async def http_put(self, path, body):
        return await self.token_client.put(path, json=body)

    async def http_delete(self, path):
        return await self.token_client.delete(path)

    async def http_patch(self, path, body):
        return await self.token_client.patch(path, json=body)

    async def http_head(self, path):
        return await self.token_client.request("HEAD", path)

    async def http_options(self, path):
        return await self.token_client.request("OPTIONS", path)

    async def close(self) -> None:
        await self.token_client.aclose()


