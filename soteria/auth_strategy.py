# Authentication
## Authentication Strategy Protocol
from typing import Dict, Protocol

class AuthStrategy(Protocol):
    async def attach(self, request_headers: Dict[str, str]) -> None:
        """
        Mutates request_headers to add whatever authentication protocol is needed for auth.
        Called on every request
        """
        ...
