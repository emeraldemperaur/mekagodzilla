from dataclasses import dataclass
from soteria.auth_strategy import AuthStrategy
from typing import Dict

@dataclass
class BearerTokenAuth(AuthStrategy):
    token: str

    async def attach(self, request_headers: Dict[str, str]) -> None:
        request_headers["Authorization"] = f"Bearer {self.token}"
