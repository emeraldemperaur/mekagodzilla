## Authentication Strategies
from dataclasses import dataclass
from soteria.auth_strategy import AuthStrategy
from typing import Dict

@dataclass
class ApiKeyAuth(AuthStrategy):
    key: str
    header_name: str = "X-API-Key"
    in_query: bool = False

    async def attach(self, request_headers: Dict[str, str]) -> None:
        if not self.in_query:
            request_headers[self.header_name] = self.key