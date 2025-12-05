# Watchtower Reporting
from artificer.artificer import ASCI_BLUE, ASCI_RESET, ASCI_ARROW, ASCI_TEAL
import logging
from logging_loki import LokiHandler
from artisan.artisan import Artisan
import os
from moneta.moneta import Moneta
from requests.exceptions import ConnectionError, Timeout
from dotenv import load_dotenv

load_dotenv(verbose=True)
system_info = Artisan()
VERSION = os.getenv("VERSION", "MekaGodzilla")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
home_directory = os.path.expanduser("~")
documents_folder = os.path.join(home_directory, "Documents")
rpa_directory_name = os.getenv("RPA_DIRECTORY_NAME", "TruliooME")
db_subdirectory_name = os.getenv("RPA_DB_SUBDIRECTORY", "Moneta")
rpa_directory_path = os.path.join(documents_folder, rpa_directory_name)
if system_info.platform.__contains__("Windows"):
    db_subdirectory_path = os.path.join(rpa_directory_path, db_subdirectory_name)
else:
    db_subdirectory_path = os.path.join(rpa_directory_path, F'.{db_subdirectory_name}')

class Heimdall:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If no instance exists, create a new one using the parent's __new__
            cls._instance = super(Heimdall, cls).__new__(cls)
        return cls._instance  # Always return the existing instance

    def __init__(self):
        try:
            os.makedirs(db_subdirectory_path, exist_ok=True)
            if system_info.platform.__contains__("Windows"):
                os.system(f'attrib +h "{db_subdirectory_path}"')
        except OSError as e:
            print(f"Heimdall encountered error creating TruliooME Data Persistence: {e}")
        log_file_path = os.path.join(Moneta.get_db_directory(), "heimdall.log")
        log_file_handler = logging.FileHandler(log_file_path)
        log_file_handler.setLevel(logging.INFO)
        log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(threadName)s')
        log_file_handler.setFormatter(log_formatter)
        if not hasattr(self, '_initialized'):
            logging.raiseExceptions = False
            self.logger = logging.getLogger("Heimdall Watchtower")
            self.logger.setLevel(logging.INFO)
            self.version = VERSION
            self.environment = ENVIRONMENT
            self.logger.addHandler(log_file_handler)
            self.loki = self.get_loki_handler(ragnarok=True)
            self._initialized = True

    @staticmethod
    def init_log():
        print(F"{ASCI_BLUE}{ASCI_ARROW} Heimdall Initialized{ASCI_RESET}")

    def info_log(self, message):
        self.logger.info(message, extra={'system name': system_info.userid})

    async def warning_log(self, message):
        self.logger.warning(message, extra={'system name': system_info.userid})

    def error_log(self, message):
        self.logger.error(message, extra={'system name': system_info.userid})

    def critical_log(self, message):
        self.logger.critical(message, extra={'system name': system_info.userid})

    def debug_log(self, message):
        self.logger.debug(message , extra={'system name': system_info.userid})

    def get_loki_handler(self, ragnarok):
        if not ragnarok:
            try:
                loki = LokiHandler(
                    url='http://localhost:3100',
                    tags={
                        "application": "TruliooME",
                        F"version": f"{self.version}::1.0",
                        F"environment": f"{self.environment}t",
                        F"os platform": {system_info.platform},
                        F"system name": {system_info.userid}
                        })
                loki.setLevel(logging.INFO)
                self.logger.addHandler(loki)
                self.info_log(F"Connecting to Grafana Loki server...")
                return loki
            except (ConnectionRefusedError, ConnectionError, Timeout) as e:
                print(F"\t{ASCI_TEAL}Heimdall encountered an error connecting to Grafana Loki: {e}{ASCI_RESET}")
                self.critical_log(F"Heimdall encountered an error connecting to Grafana Loki: {e}")
                return None
            except Exception as e:
                print(F"\t{ASCI_TEAL}Heimdall encountered an error connecting to Grafana Loki: {e}{ASCI_RESET}")
                self.critical_log(F"Heimdall encountered an error connecting to Grafana Loki: {e}")
                return None
        else:
            return None




