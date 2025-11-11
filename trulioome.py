# Trulioo SME Logic
from artificer import ASCI_GREEN, ASCI_RESET, ASCI_ONLINE
from artisan import Artisan


class TruliooME:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If no instance exists, create a new one using the parent's __new__
            cls._instance = super(TruliooME, cls).__new__(cls)
        return cls._instance  # Always return the existing instance

    def __init__(self, heimdall):
        if not hasattr(self, '_initialized'):
            self.artisan = Artisan()
            self.heimdall = heimdall
            self._initialized = True
            self.heimdall.info_log(F"Initialized TruliooME Agent Core::{self.artisan.date}")
            print(F'{ASCI_GREEN}{ASCI_ONLINE} TruliooME Activated{ASCI_RESET}\n')

