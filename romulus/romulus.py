# Productivity Tools Interface Module 2
import uuid
from artificer.artificer import ASCI_BLUE, ASCI_RESET, ASCI_ARROW
from artisan.artisan import Artisan


class Romulus:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If no instance exists, create a new one using the parent's __new__
            cls._instance = super(Romulus, cls).__new__(cls)
        return cls._instance  # Always return the existing instance

    def __init__(self, heimdall):
        if not hasattr(self, '_initialized'):
            self.artisan = Artisan()
            self.heimdall = heimdall
            self._initialized = True
            self.heimdall.info_log(F"Initialized Romulus Productivity Module::@{uuid.uuid4()}")
            print(F"{ASCI_BLUE}{ASCI_ARROW} Romulus Initialized{ASCI_RESET}")