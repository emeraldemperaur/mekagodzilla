# Trulioo API Interface Interactions
from __future__ import annotations
from artificer.artificer import ASCI_BLUE, ASCI_RESET, ASCI_ARROW
from artisan.artisan import Artisan
# from soteria.hmac_auth import HMACAuth
# from soteria.api_error import ApiError
# from soteria.auth_strategy import AuthStrategy
# from soteria.api_key_auth import ApiKeyAuth
# from soteria.bearer_token_auth import BearerTokenAuth
# from soteria.oauth2_client_credentials import OAuth2ClientCredentials
# from soteria.api_client import ApiClient

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







