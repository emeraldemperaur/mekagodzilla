from soteria.auth_strategy import AuthStrategy
import hashlib
import base64
import hmac
from typing import Dict
import time
from dataclasses import dataclass

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