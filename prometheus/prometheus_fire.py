import time
from typing import Optional
from selenium import webdriver
from dotenv import load_dotenv
import os
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver

from artificer.artificer import ASCI_GREEN, ASCI_RESET, ASCI_PROMETHEUS, ASCI_TEAL, ASCI_OHM
from heimdall.heimdall import Heimdall
from moneta.moneta import Moneta
from prometheus.prometheus_forge import Prometheum
from trulioome.trulioome import TruliooME

load_dotenv(verbose=True)
chrome_options = ChromeOptions()
firefox_options = FirefoxOptions()
if os.getenv("PROMETHEUS_HEADLESS_MODE") == "True":
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--start-maximized")
    firefox_options.add_argument("--headless")
preferences = {
    "download.default_directory": F"{Moneta.get_server_downloads_directory()}",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}

class PrometheusFire:
    """
           Creates an instance of the Selenium WebDriver with prometheus_driver
           """
    def __init__(self, headless: Optional[bool] = False, browser_name: Optional[str] = None,
                 heimdall: Optional[Heimdall] = None, fullscreen: Optional[bool] = False):
        """
        Initialize an instance of the Selenium WebDriver with prometheus_driver

        :param headless:
        :param browser_name:
        :param heimdall:
        :param fullscreen:
        """
        self.headless = headless
        self.fullscreen = fullscreen
        self.prometheus_webdriver = None
        self.bench_webdriver = None
        self.chrome_options = ChromeOptions()
        self.firefox_options = FirefoxOptions()
        self.bench_options = ChromeOptions()
        self.bench_count = 0
        self.heimdall = heimdall
        self.chrome_options.add_experimental_option("prefs", preferences)
        if os.getenv("DISABLE_DOWNLOAD_PROTECTION") == "True":
            self.chrome_options.add_argument("--safebrowsing-disable-download-protection")
        if headless or os.getenv("PROMETHEUS_HEADLESS_MODE") == "True":
            self.chrome_options.add_argument("--headless=new")
            self.firefox_options.add_argument("--headless")
        if browser_name is not None:
            match browser_name.lower():
                case "chrome":
                    self.prometheus_webdriver = webdriver.Chrome(options=self.chrome_options)
                    print(F"\n{ASCI_GREEN}{ASCI_PROMETHEUS} Prometheus RPA Driver :: Chrome{ASCI_RESET}")
                    self.heimdall.info_log(F"{ASCI_GREEN}{ASCI_PROMETHEUS} Prometheus RPA Driver :: Chrome{ASCI_RESET}")
                case "firefox":
                    self.prometheus_webdriver = webdriver.Firefox(options=self.firefox_options)
                    print(F"\n{ASCI_GREEN}{ASCI_PROMETHEUS} Prometheus RPA Driver :: Firefox{ASCI_RESET}")
                    self.heimdall.info_log(F"{ASCI_GREEN}{ASCI_PROMETHEUS} Prometheus RPA Driver :: Firefox{ASCI_RESET}")
                case "edge":
                    self.prometheus_webdriver = webdriver.Edge(options=self.chrome_options)
                    print(F"\n{ASCI_GREEN}{ASCI_PROMETHEUS} Prometheus RPA Driver :: Edge{ASCI_RESET}")
                    self.heimdall.info_log(F"{ASCI_GREEN}{ASCI_PROMETHEUS} Prometheus RPA Driver :: Edge{ASCI_RESET}")
                case _:  # Default case, similar to 'else'
                    self.prometheus_webdriver = webdriver.Chrome(options=self.chrome_options)
                    print(F"\n{ASCI_GREEN}{ASCI_PROMETHEUS} Prometheus RPA Driver :: Chrome{ASCI_RESET}")
                    self.heimdall.info_log(F"{ASCI_GREEN}{ASCI_PROMETHEUS} Prometheus RPA Driver :: Chrome{ASCI_RESET}")
        else:
            self.prometheus_webdriver = webdriver.Chrome(options=self.chrome_options)
            print(F"\n{ASCI_GREEN}{ASCI_PROMETHEUS} Prometheus RPA Driver :: Chrome{ASCI_RESET}")

    async def get_url(self, url: str) -> WebDriver:
        """
        Calls a webpage url address via default Selenium WebDriver
        :param url:
        :return: Selenium WebDriver instance
        """
        self.prometheus_webdriver.get(url)
        if self.fullscreen:
            self.prometheus_webdriver.fullscreen_window()
        print(F"\t{ASCI_TEAL}{ASCI_OHM} Prometheus Fire :: Get URL ({url}){ASCI_RESET}")
        self.heimdall.info_log(F"\t{ASCI_TEAL}{ASCI_OHM} Prometheus Fire :: Get URL ({url}){ASCI_RESET}")
        return self.prometheus_webdriver

    async def get_prometheus_webdriver(self) -> WebDriver:
        return self.prometheus_webdriver

    async def set_prometheus_webdriver_by_name(self, browser_name: str) -> WebDriver:
        match browser_name.lower():
            case "chrome":
                self.prometheus_webdriver = webdriver.Chrome(options=self.chrome_options)
                print(F"\n{ASCI_GREEN}{ASCI_PROMETHEUS} Prometheus RPA Driver :: Chrome{ASCI_RESET}")
                self.heimdall.info_log(F"{ASCI_GREEN}{ASCI_PROMETHEUS} Prometheus RPA Driver :: Chrome{ASCI_RESET}")
            case "firefox":
                self.prometheus_webdriver = webdriver.Firefox(options=self.firefox_options)
                print(F"\n{ASCI_GREEN}{ASCI_PROMETHEUS} Prometheus RPA Driver :: Firefox{ASCI_RESET}")
                self.heimdall.info_log(F"{ASCI_GREEN}{ASCI_PROMETHEUS} Prometheus RPA Driver :: Firefox{ASCI_RESET}")
            case "edge":
                self.prometheus_webdriver = webdriver.Edge(options=self.chrome_options)
                print(F"\n{ASCI_GREEN}{ASCI_PROMETHEUS} Prometheus RPA Driver :: Edge{ASCI_RESET}")
                self.heimdall.info_log(F"{ASCI_GREEN}{ASCI_PROMETHEUS} Prometheus RPA Driver :: Edge{ASCI_RESET}")
            case _:  # Default case, similar to 'else'
                self.prometheus_webdriver = webdriver.Chrome(options=self.chrome_options)
                print(F"\n{ASCI_GREEN}{ASCI_PROMETHEUS} Prometheus RPA Driver :: Chrome{ASCI_RESET}")
                self.heimdall.info_log(F"{ASCI_GREEN}{ASCI_PROMETHEUS} Prometheus RPA Driver :: Chrome{ASCI_RESET}")
        return self.prometheus_webdriver

    async def get_bench_webdriver(self, headless: Optional[bool] = False) -> WebDriver:
        if headless:
            self.bench_options.add_argument("--headless=new")
        self.bench_webdriver = webdriver.Chrome(options=self.bench_options)
        self.bench_count += 1
        print(F"\n{ASCI_GREEN}{ASCI_PROMETHEUS} Prometheus RPA Bench Driver :: ({self.bench_count}){ASCI_RESET}")
        return self.bench_webdriver

    async def global_gateway_login(self, username: str, password: str, auth_mode: Optional[int] = 1,
                                   web_driver: Optional[WebDriver] = None,
                                   heimdall: Optional[Heimdall] = None) -> tuple[WebDriver, bool]:
        if web_driver is None:
            web_driver = await self.get_prometheus_webdriver()
        trulioo_me = TruliooME(heimdall=heimdall, web_driver=web_driver)
        this_webdriver = await trulioo_me.tacos_create_account_demo(username=username,
                                            password=password,
                                            auth_mode=auth_mode)
        return this_webdriver[0], this_webdriver[1]

    async def client_portal_login(self, username: str, password: str,
                                  web_driver: Optional[WebDriver] = None) -> WebDriver:
        if web_driver is None:
            web_driver = await self.get_prometheus_webdriver()
        web_driver.get("https://portal.trulioo.com/Account/LogOn")
        web_driver.maximize_window()
        sso_login_button = web_driver.find_element(By.LINK_TEXT, "Log in with Single Sign-On (SSO)")
        if sso_login_button:
            sso_login_button.click()
        email_input = web_driver.find_element(By.ID, "username")
        email_input.send_keys(username)
        login_button = web_driver.find_element(By.ID, "btn-sso-login")
        login_button.click()
        time.sleep(3)
        if web_driver.title == "Sign in - Google Accounts":
            g_username = web_driver.find_element(By.ID, "identifierId")
            g_username.send_keys(username)
            next_button = web_driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button')
            if next_button:
                next_button.click()
            time.sleep(6)
            if web_driver.title == "Welcome":
                password_input = web_driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
                password_input.send_keys(password)
                nxt_button = web_driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button')
                if nxt_button:
                    nxt_button.click()
        return web_driver

    async def elementfinder(self) -> Prometheum:
        element_finder = Prometheum(webdriver=self.prometheus_webdriver)
        return element_finder

    @staticmethod
    async def get_elementfinder(prometheus_webdriver: WebDriver) -> Prometheum:
        element_finder = Prometheum(webdriver=prometheus_webdriver)
        return element_finder








