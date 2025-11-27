# Base User Interface Interactions
import time
from typing import Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from artificer.artificer import ASCI_BLUE, ASCI_RESET, ASCI_ARROW
from artisan.artisan import Artisan
from imhotep.imhotep import Imhotep
from heimdall.heimdall import Heimdall
from mercurius.mercurius import Mercurius
from mercury.mercury import Mercury
from minerva.minerva import Minerva
from moneta.moneta import Moneta
from remus.remus import Remus
from romulus.romulus import Romulus
from securitas.securitas import Securitas
from soteria.soteria import Soteria
from trulioome.trulioome import TruliooME
from selenium import webdriver
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
chrome_options = ChromeOptions()
firefox_options = FirefoxOptions()
if os.getenv("PROMETHEUS_HEADLESS_MODE") == "True":
    chrome_options.add_argument("--headless=new")
    firefox_options.add_argument("--headless")

class Prometheus:
    _instance = None
    _artisan = Artisan()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If no instance exists, create a new one using the parent's __new__
            cls._instance = super(Prometheus, cls).__new__(cls)
        return cls._instance  # Always return the existing instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            print(F"\n{ASCI_BLUE}{ASCI_ARROW} Prometheus Initialized{ASCI_RESET}")
            self.heimdall = Heimdall()
            Heimdall.init_log()
            self.artisan = Artisan()
            self.heimdall.info_log(F"Prometheus Initialized::{self.artisan.userid}")
            self.imhotep = Imhotep(self.heimdall)
            self.mercurius = Mercurius()
            self.heimdall.info_log(F"Mercurius API Server Activated::{self.artisan.platform}")
            self.mercurius.init_log()
            self.mercury = Mercury()
            self.mercury.init_log(ASCI_BLUE, ASCI_ARROW, " Initialized")
            self.minerva = Minerva(self.heimdall)
            self.moneta = Moneta(self.heimdall)
            self.remus = Remus(self.heimdall)
            self.romulus = Romulus(self.heimdall)
            self.securitas = Securitas(self.heimdall)
            self.soteria = Soteria(self.heimdall)
            self.trulioome = TruliooME(self.heimdall)
            self._initialized = True

    @staticmethod
    def get_webdriver_by_name(browser_name: Optional[str] = None) -> WebDriver:
        prometheus_driver = None
        match browser_name.lower():
            case "chrome":
                prometheus_driver = webdriver.Chrome(options=chrome_options)
            case "firefox":
                prometheus_driver = webdriver.Firefox(options=firefox_options)
            case "edge":
                prometheus_driver = webdriver.Edge(options=chrome_options)
                print("Value is the string 'edge'.")
            case _:  # Default case, similar to 'else'
                prometheus_driver = webdriver.Chrome(options=chrome_options)
        return prometheus_driver

    @staticmethod
    def get_webdriver() -> WebDriver:
        prometheus_driver = None
        match os.getenv("PROMETHEUS_DEFAULT_DRIVER").lower():
            case "chrome":
                prometheus_driver = webdriver.Chrome(options=chrome_options)
                print("Value is chrome.")
            case "firefox":
                prometheus_driver = webdriver.Firefox(options=firefox_options)
                print("Value is firefox.")
            case "edge":
                prometheus_driver = webdriver.Edge(options=chrome_options)
            case _:  # Default case, similar to 'else'
                prometheus_driver = webdriver.Chrome(options=chrome_options)
                print("Value does not match any specific browser.")
        return prometheus_driver

    @staticmethod
    def get_webpage(url):
        prometheus_webdriver = Prometheus.get_webdriver()
        prometheus_webdriver.get(url)
        return prometheus_webdriver

