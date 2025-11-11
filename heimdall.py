# Watchtower Reporting
from artificer import ASCI_BLUE, ASCI_RESET, ASCI_ARROW, ASCI_TEAL
import logging
from logging_loki import LokiHandler
from artisan import Artisan
import os
from moneta import Moneta
from requests.exceptions import ConnectionError, Timeout

system_info = Artisan()
log_file_path = os.path.join(Moneta.get_db_directory(), "heimdall.log")
log_file_handler = logging.FileHandler(log_file_path)
log_file_handler.setLevel(logging.INFO)
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(threadName)s')
log_file_handler.setFormatter(log_formatter)

class Heimdall:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If no instance exists, create a new one using the parent's __new__
            cls._instance = super(Heimdall, cls).__new__(cls)
        return cls._instance  # Always return the existing instance

    def __init__(self, version, environment):
        if not hasattr(self, '_initialized'):
            logging.raiseExceptions = False
            self.logger = logging.getLogger("Heimdall Watchtower")
            self.logger.setLevel(logging.INFO)
            self.version = version
            self.environment = environment
            self.logger.addHandler(log_file_handler)
            self.loki = self.get_loki_handler(ragnarok=True)
            self._initialized = True
            # print(F"{ASCI_BLUE}{ASCI_ARROW} Heimdall Initialized{ASCI_RESET}")

    @staticmethod
    def init_log():
        print(F"{ASCI_BLUE}{ASCI_ARROW} Heimdall Initialized{ASCI_RESET}")

    def info_log(self, message):
        self.logger.info(message, extra={'system name': system_info.userid})

    def warning_log(self, message):
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




