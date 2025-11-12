# Command Line Interface
import uuid
from artificer.artificer import ASCI_BLUE, ASCI_ARROW, ASCI_RESET
from artisan.artisan import Artisan


class Minerva:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If no instance exists, create a new one using the parent's __new__
            cls._instance = super(Minerva, cls).__new__(cls)
        return cls._instance  # Always return the existing instance

    def __init__(self, heimdall):
        if not hasattr(self, '_initialized'):
            self.artisan = Artisan()
            self.heimdall = heimdall
            self._initialized = True
            self.heimdall.info_log(F"Initialized Minerva CLI::@{uuid.uuid4()}")
            print(F"{ASCI_BLUE}{ASCI_ARROW} Minerva Initialized{ASCI_RESET}")