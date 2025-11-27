import asyncio
import os
from typing import Optional, Dict

from soteria.api_client import ApiClient
from soteria.api_key_auth import ApiKeyAuth
from soteria.api_error import ApiError
from dotenv import load_dotenv

load_dotenv(verbose=True)

class ApiClientKeyQueryAuth(ApiKeyAuth):
    def __init__(self, base_url: str, *, api_key: Optional[str] = None, param_name: str = "api_key",) -> None:
        self.base_url = base_url.rstrip("/")
        self.param_name = param_name
        self.api_key = api_key or os.getenv("SOTERIA_API_KEY")
        if not self.api_key:
            raise ValueError("SOTERIA_API_KEY environment variable not set")
        self.api_keyq_client = ApiClient(base_url=self.base_url,
                                auth=ApiKeyAuth(key=self.api_key, in_query=True),
                                default_params={self.param_name: self.api_key},
                                max_retries=3, backoff_factor=0.5,)

    async def set_api_key(self, new_api_key: str) -> None:
        """
             Reset the API key at runtime
             :param new_api_key:
             :return: None
             """
        if not new_api_key:
            raise ValueError("SOTERIA_API_KEY environment variable not set")
        self.api_key = new_api_key
        self.api_keyq_client.auth = ApiKeyAuth(key=self.api_key, in_query=True)
        self.api_keyq_client.default_params[self.param_name] = self.api_key

    async def http_get(self, path, params:Optional[Dict[str, str]]=None):
        return await self.api_keyq_client.get(path, params=params)

    async def http_post(self, path, body):
        return await self.api_keyq_client.post(path, body=body)

    async def http_put(self, path, body):
        return await self.api_keyq_client.put(path, body=body)

    async def http_delete(self, path):
        return await self.api_keyq_client.delete(path)

    async def http_patch(self, path, body):
        return await self.api_keyq_client.patch(path, body=body)

    async def http_options(self, path):
        return await self.api_keyq_client.request("OPTIONS", path)

    async def http_head(self, path):
        return await self.api_keyq_client.request("HEAD", path)

    async def close(self) -> None:
        await self.api_keyq_client.aclose()
