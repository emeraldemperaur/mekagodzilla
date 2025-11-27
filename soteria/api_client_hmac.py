import asyncio
from typing import Optional, Dict

from soteria.api_client import ApiClient
from soteria.hmac_auth import HMACAuth
from soteria.api_error import ApiError

class ApiClientHMAC(HMACAuth):
    """
    Stores an HMAC key_id + secret in memory and signs every request.
    """
    def __init__(self, key, base_url: str, key_id: str, secret: str) -> None:
        if not key_id or not secret:
            raise ValueError("Both key_id and secret are required")
        self.base_url = base_url.rstrip("/")
        self.key_id = key_id
        self.secret = secret
        self.hmac_client = ApiClient(base_url=self.base_url, auth=HMACAuth(key_id=self.key_id, secret=self.secret),
                                     max_retries=3, backoff_factor=0.5,)

    def reset_keys(self, key_id: str, secret: str) -> None:
        """
        Reset HMAC key_id + secret at runtime
        :param key_id:
        :param secret:
        :return:
        """
        if not key_id or not secret:
            raise ValueError("Both key_id and secret are required")
        self.key_id = key_id
        self.secret = secret
        self.hmac_client.auth = HMACAuth(key_id=self.key_id, secret=self.secret)

    async def http_get(self, path, params:Optional[Dict[str, str]]=None):
        await self.hmac_client.get(path, params=params)

    async def http_post(self, path, body):
        await self.hmac_client.post(path, body=body)

    async def http_put(self, path, body):
        await self.hmac_client.put(path, body=body)

    async def http_delete(self, path):
        await self.hmac_client.delete(path)

    async def http_patch(self, path, body):
        await self.hmac_client.patch(path, body=body)

    async def http_options(self, path):
        await self.hmac_client.request("OPTIONS", path)

    async def http_head(self, path):
        await self.hmac_client.request("HEAD", path)

    async def close(self) -> None:
        await self.hmac_client.aclose()

