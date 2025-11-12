# Utility Methods
import getpass
import platform
import textwrap
from datetime import datetime
from artificer.artificer import ASCI_LOGO, ASCI_ITALIC, ASCI_BOLD, ASCI_RESET, RAG_CONTEXT, ASCI_GREEN, ASCI_RED, ASCI_BLUE

class Artisan:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If no instance exists, create a new one using the parent's __new__
            cls._instance = super(Artisan, cls).__new__(cls, *args, **kwargs)
        return cls._instance  # Always return the existing instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.platform = platform.platform(aliased=True)
            self.timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            self.date = datetime.now().strftime("%A %B %d, %Y")
            self.time = datetime.now().strftime("%H:%M:%S")
            try:
                username = getpass.getuser()
                self.userid = username

            except Exception as e_getpass:
                print(f"{ASCI_RED}Error ({e_getpass}). Could not determine system UserId{ASCI_RESET}")
                self.userid = "Guest"
            self._initialized = True

    @staticmethod
    def rag_context_wrap(rag_context):
        return textwrap.fill(rag_context, width=96)

    @staticmethod
    def get_platform():
        return platform.platform(aliased=True)

    @staticmethod
    def console_output(version, system):
        if version == 'MekaGodzilla':
            print(f'{ASCI_GREEN}{ASCI_LOGO}{ASCI_RESET}'
                  f'{ASCI_BLUE}{ASCI_ITALIC}Running Truliooᴹᴱ Robotic Process Automation Server...{ASCI_RESET}\n'
                  f'{ASCI_BOLD}Version ID{ASCI_RESET}: {version}\n'
                  f'{ASCI_BOLD}OS Platform{ASCI_RESET}: {system.platform}\n'
                  f'{ASCI_BOLD}UserID{ASCI_RESET}: {system.userid}\n'
                  f'{ASCI_BOLD}Timestamp{ASCI_RESET}: {system.timestamp} | {system.date}')
        else:
            print(f'{ASCI_GREEN}{ASCI_LOGO}{ASCI_RESET}'
                  f'{ASCI_BLUE}{ASCI_ITALIC}Executing Truliooᴹᴱ Robotic Process Automation...{ASCI_RESET}\n'
                  f'{ASCI_BOLD}Version ID{ASCI_RESET}: {version}\n'
                  f'{ASCI_BOLD}OS Platform{ASCI_RESET}: {system.platform}\n'
                  f'{ASCI_BOLD}Domain{ASCI_RESET}: Portal Configuration\n'
                  f'{ASCI_BOLD}Process{ASCI_RESET}: New Account Setup - Enterprise\n'
                  f'{ASCI_BOLD}UserID{ASCI_RESET}: {system.userid}\n'
                  f'{ASCI_BOLD}Timestamp{ASCI_RESET}: {system.timestamp} | {system.date} \n'
                  f'{ASCI_BOLD}RAG Context{ASCI_RESET}: {system.rag_context_wrap(RAG_CONTEXT)}')
