# Trulioo SME Logic
from typing import Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from artificer.artificer import ASCI_GREEN, ASCI_RESET, ASCI_ONLINE, ASCI_TEAL, ASCI_OHM, ASCI_RED
from artisan.artisan import Artisan
from artisan.hermes import Hermes
from heimdall.heimdall import Heimdall
from prometheus.prometheus_forge import Prometheum


class TruliooME:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If no instance exists, create a new one using the parent's __new__
            cls._instance = super(TruliooME, cls).__new__(cls)
        return cls._instance  # Always return the existing instance

    def __init__(self, heimdall: Heimdall, web_driver: Optional[WebDriver] = None):
        if web_driver is not None:
            self.webdriver = web_driver
            self.globalgateway_username = None
            self.globalgateway_password = None
            self.clientadmin_username = None
            self.clientadmin_password = None
        if not hasattr(self, '_initialized'):
            self.artisan = Artisan()
            self.heimdall = heimdall
            self._initialized = True
            self.heimdall.info_log(F"Initialized TruliooME Agent Core::{self.artisan.date}")
            print(F'{ASCI_GREEN}{ASCI_ONLINE} TruliooME Activated{ASCI_RESET}\n')

    async def global_gateway_login(self, username: str, password: str,
                                   heimdall: Heimdall,
                                   auth_mode: Optional[int] = 1,
                                   web_driver: Optional[WebDriver] = None,
                                   ) -> tuple[WebDriver, bool]:
        print(F"\t{ASCI_TEAL}{ASCI_OHM} TruliooME Agent Core :: Global Gateway Login ({username}){ASCI_RESET}")
        self.heimdall.info_log(F"TruliooME Agent Core ::  Global Gateway Login ({username}) @ {self.artisan.timestamp}")
        self.globalgateway_username = username
        self.globalgateway_password = password
        if web_driver is None:
            web_driver = self.webdriver
        web_driver.maximize_window()
        web_driver.get("https://adminportal.trulioo.com/Account/LogOn")
        element_forge = Prometheum(webdriver=web_driver)
        username_field = element_forge.get_element_by(locator_strategy="id", locator_value="UserName")
        password_field = element_forge.get_element_by(locator_strategy="id", locator_value="Password")
        sign_in_button = element_forge.get_element_by(locator_strategy="name", locator_value="submit-login")
        username_field.send_keys(username)
        password_field.send_keys(password)
        sign_in_button.click()
        send_me_push_xpath = "//button[normalize-space()='Send Me a Push']"
        xpath_call = "//button[normalize-space()='Call Me']"
        xpath_code = "//button[@id='passcode']"
        auth_xpath = None
        if auth_mode == 1:
            auth_xpath = send_me_push_xpath
        elif auth_mode == 2:
            auth_xpath = xpath_call
        elif auth_mode == 3:
            auth_xpath = xpath_code
        if element_forge.page_title_is("TwoFactor"):
            duo_iframe = element_forge.get_element_by(locator_strategy="xpath", locator_value="//*[@id='duo_iframe']")
            web_driver.switch_to.frame(duo_iframe)
            duo_auth_button = element_forge.get_element_by(locator_strategy="xpath", locator_value=auth_xpath)
            duo_auth_button.click()
            web_driver.switch_to.default_content()
            if element_forge.page_title_is("Tacos"):
                tacos_admin_button = element_forge.get_element_by(
                    locator_strategy="linktext",
                    locator_value="TACOS (Trulioo Administration and Customer Onboarding System)")
                tacos_admin_button.click()
                create_account_menu_button = element_forge.get_element_by(
                    locator_strategy="xpath",
                    locator_value="//*[@id='sidebar']/div/div[2]/a[1]/div/div")
                create_account_menu_button.click()
                if element_forge.page_title_is("Tacos Account Creation"):
                    name = "MekaGodzilla Test" or "Mekatron Test"
                    account_name_field = element_forge.get_element_by(locator_strategy="xpath",
                                                                      locator_value='//*[@id="AccountName"]')
                    isinternal_toggle = element_forge.get_element_by(
                        locator_strategy="xpath",
                        locator_value='//*[@id="isInternal-toggle"]/label/span[1]')
                    issandbox_toggle = element_forge.get_element_by(
                        locator_strategy="xpath",
                        locator_value='//*[@id="isSandboxEnv-toggle"]/label/span[1]')
                    if account_name_field:
                        account_name_field.send_keys(name)
                    if isinternal_toggle:
                        isinternal_toggle.click()
                    if issandbox_toggle:
                        issandbox_toggle.click()
        if self.heimdall:
            self.heimdall.info_log(F"\t{ASCI_TEAL}{ASCI_OHM} TruliooME Agent Core :: "
                              F"Global Gateway Login ({username}){ASCI_RESET})")
        return web_driver, True

    async def global_gateway_tacos_login(self, username: str, password: str, auth_mode: Optional[int] = 1,
                                   web_driver: Optional[WebDriver] = None,
                                   heimdall: Optional[Heimdall] = None) -> tuple[WebDriver, bool]:
        print(F"\t{ASCI_TEAL}{ASCI_OHM} TruliooME Agent Core :: Global Gateway Login ({username}){ASCI_RESET}")
        self.heimdall.info_log(F"TruliooME Agent Core ::  Global Gateway Login ({username}) @ {self.artisan.timestamp}")
        self.globalgateway_username = username
        self.globalgateway_password = password
        if web_driver is None:
            web_driver = self.webdriver
        web_driver.get("https://adminportal.trulioo.com/Account/LogOn")
        web_driver.maximize_window()
        element_forge = Prometheum(webdriver=web_driver)
        username_field = element_forge.get_element_by(locator_strategy="id", locator_value="UserName")
        password_field = element_forge.get_element_by(locator_strategy="id", locator_value="Password")
        sign_in_button = element_forge.get_element_by(locator_strategy="name", locator_value="submit-login")
        username_field.send_keys(username)
        password_field.send_keys(password)
        sign_in_button.click()
        send_me_push_xpath = "//button[normalize-space()='Send Me a Push']"
        xpath_call = "//button[normalize-space()='Call Me']"
        xpath_code = "//button[@id='passcode']"
        auth_xpath = None
        if auth_mode == 1:
            auth_xpath = send_me_push_xpath
        elif auth_mode == 2:
            auth_xpath = xpath_call
        elif auth_mode == 3:
            auth_xpath = xpath_code
        if element_forge.page_title_is("TwoFactor"):
            duo_iframe = element_forge.get_element_by(locator_strategy="xpath", locator_value="//*[@id='duo_iframe']")
            web_driver.switch_to.frame(duo_iframe)
            duo_auth_button = element_forge.get_element_by(locator_strategy="xpath", locator_value=auth_xpath)
            duo_auth_button.click()
            web_driver.switch_to.default_content()
            if element_forge.page_title_is("Tacos"):
                tacos_admin_button = element_forge.get_element_by(
                    locator_strategy="linktext",
                    locator_value="TACOS (Trulioo Administration and Customer Onboarding System)")
                tacos_admin_button.click()
        if self.heimdall and element_forge.page_title_is("Tacos"):
            self.heimdall.info_log(F"\t{ASCI_TEAL}{ASCI_OHM} TruliooME Agent Core :: "
                              F"Global Gateway Tacos Login ({username}){ASCI_RESET})")
        elif self.heimdall and not element_forge.page_title_is("Tacos"):
            self.heimdall.error_log(F"\t{ASCI_TEAL}{ASCI_OHM} TruliooME Agent Core :: "
                              F"Global Gateway Tacos Login ({username}) Failed{ASCI_RESET})")
        return web_driver, element_forge.page_title_is("Tacos")

    async def global_gateway_legacy_login(self, username: str, password: str, auth_mode: Optional[int] = 1,
                                   web_driver: Optional[WebDriver] = None,
                                   heimdall: Optional[Heimdall] = None) -> tuple[WebDriver, bool]:
        print(F"\t{ASCI_TEAL}{ASCI_OHM} TruliooME Agent Core :: Global Gateway Legacy Login ({username}){ASCI_RESET}")
        self.heimdall.info_log(F"TruliooME Agent Core ::  Global Gateway Legacy Login ({username}) "
                               F"@ {self.artisan.timestamp}")
        self.globalgateway_username = username
        self.globalgateway_password = password
        if web_driver is None:
            web_driver = self.webdriver
        web_driver.get("https://adminportal.trulioo.com/Account/LogOn")
        web_driver.maximize_window()
        element_forge = Prometheum(webdriver=web_driver)
        username_field = element_forge.get_element_by(locator_strategy="id", locator_value="UserName")
        password_field = element_forge.get_element_by(locator_strategy="id", locator_value="Password")
        sign_in_button = element_forge.get_element_by(locator_strategy="name", locator_value="submit-login")
        username_field.send_keys(username)
        password_field.send_keys(password)
        sign_in_button.click()
        send_me_push_xpath = "//button[normalize-space()='Send Me a Push']"
        xpath_call = "//button[normalize-space()='Call Me']"
        xpath_code = "//button[@id='passcode']"
        auth_xpath = None
        if auth_mode == 1:
            auth_xpath = send_me_push_xpath
        elif auth_mode == 2:
            auth_xpath = xpath_call
        elif auth_mode == 3:
            auth_xpath = xpath_code
        if element_forge.page_title_is("TwoFactor"):
            duo_iframe = element_forge.get_element_by(locator_strategy="xpath", locator_value="//*[@id='duo_iframe']")
            web_driver.switch_to.frame(duo_iframe)
            duo_auth_button = element_forge.get_element_by(locator_strategy="xpath", locator_value=auth_xpath)
            duo_auth_button.click()
            web_driver.switch_to.default_content()
            if element_forge.page_title_is("Tacos", timeout=60):
                legacy_admin_button = element_forge.get_element_by(
                    locator_strategy="linktext",
                    locator_value="Admin Portal")
                legacy_admin_button.click()
                if element_forge.page_title_is("Index"):
                    self.heimdall.info_log(F"\t{ASCI_TEAL}{ASCI_OHM} TruliooME Agent Core :: "
                              F"Global Gateway Legacy Admin Logged In ({username}){ASCI_RESET})")
                elif not element_forge.page_title_is("Tacos"):
                    self.heimdall.error_log(F"\t{ASCI_TEAL}{ASCI_OHM} TruliooME Agent Core :: "
                              F"Global Gateway Legacy Admin Login ({username}) Failed{ASCI_RESET})")
        await self.heimdall.warning_log(F"\t{ASCI_TEAL}{ASCI_OHM} TruliooME Agent Core :: "
                               F"Global Gateway Legacy Admin Logded In ({username}){ASCI_RESET})")
        return web_driver, element_forge.page_title_is("Index")

    async def tacos_create_account_demo(self, username: str, password: str,
                                        account_name: Optional[str] = None, auth_mode: Optional[int] = 1,
                                        web_driver: Optional[WebDriver] = None,
                                        heimdall: Optional[Heimdall] = None) -> tuple[WebDriver, bool]:
        is_global_gateway_logged_in = await self.global_gateway_tacos_login(username=username, password=password,
                                                                            auth_mode=auth_mode, heimdall=heimdall)
        is_complete = False
        if web_driver is None:
            web_driver = is_global_gateway_logged_in[0] or self.webdriver
        element_forge = Prometheum(webdriver=web_driver)
        if is_global_gateway_logged_in[1]:
            element_forge.capture_snapshot("Create Account Demo")
            element_forge.capture_fullscreen_snapshot("Create Account Demo", is_error=True)
            create_account_menu_button = element_forge.get_element_by(
                locator_strategy="xpath",
                locator_value="//*[@id='sidebar']/div/div[2]/a[1]/div/div")
            create_account_menu_button.click()
            if element_forge.page_title_is("Tacos Account Creation"):
                name = account_name or "MekaGodzilla Test"
                account_name_field = element_forge.get_element_by(locator_strategy="xpath",
                                                                  locator_value='//*[@id="AccountName"]')
                isinternal_toggle = element_forge.get_element_by(
                    locator_strategy="xpath",
                    locator_value='//*[@id="isInternal-toggle"]/label/span[1]')
                issandbox_toggle = element_forge.get_element_by(
                    locator_strategy="xpath",
                    locator_value='//*[@id="isSandboxEnv-toggle"]/label/span[1]')
                if account_name_field:
                    account_name_field.send_keys(name)
                if isinternal_toggle:
                    isinternal_toggle.click()
                if issandbox_toggle:
                    issandbox_toggle.click()
                    element_forge.capture_snapshot("Create Account Demo")
                if account_name_field.is_displayed():
                    is_complete = True
        if self.heimdall and is_complete:
            print(F"\t{ASCI_TEAL}{ASCI_OHM} TruliooME Agent Core :: "
                  F"Tacos Created Account Demo ({account_name or "MekaGodzilla Test"}){ASCI_RESET}")
            self.heimdall.info_log(F"\t{ASCI_TEAL}{ASCI_OHM} TruliooME Agent Core :: "
                              F"Tacos Create Account Demo ({account_name or "MekaGodzilla Test"}){ASCI_RESET})")
        elif self.heimdall and not is_complete:
            self.heimdall.error_log(F"\t{ASCI_TEAL}{ASCI_OHM} TruliooME Agent Core :: "
                              F"Tacos Create Account Demo ({account_name or "MekaGodzilla Test"}) Failed{ASCI_RESET})")
        return web_driver, is_complete

    async def workflow_client_portal_login(self, username: str, password: str) -> tuple[WebDriver, bool]:
        pass

    async def go_to_tacos_account_by_name_or_identifier(self,
                                                account_name: str,
                                                account_identifier: Optional[str] = None) -> tuple[WebDriver, bool]:
        search_value = ""
        if account_identifier:
            search_value = account_identifier
        else:
            search_value = account_name
        return self.webdriver, True

    async def go_to_legacy_account_by_name_or_identifier(self,
                                                account_name: str,
                                                account_identifier: Optional[str] = None,
                                                web_driver: Optional[WebDriver] = None) -> tuple[WebDriver, bool]:
        # search_value = ""
        is_complete = False
        if web_driver is None:
            web_driver = self.webdriver
        element_forge = Prometheum(webdriver=web_driver)
        if account_identifier:
            search_value = account_identifier
        else:
            search_value = account_name
        if element_forge.page_title_is("Index"):
            print(F"\t{ASCI_TEAL}{ASCI_OHM} TruliooME Agent Core :: Go to Global Gateway Account ({account_name})"
                  F" {ASCI_RESET}")
            accountlist_table_data = element_forge.get_table_element_data(
                locator_strategy="xpath", locator_value='//*[@id="content"]/div[1]/table',
                output_as="dataframe")
            accountlist_table_element = element_forge.get_table_element_data(
                locator_strategy="xpath", locator_value='//*[@id="content"]/div[1]/table',
                output_as="webelement")
            accountlist_table_rows = element_forge.get_table_row_elements_data(
                table_webelement=accountlist_table_element, include_header=False)
            print(F"\t{ASCI_TEAL}{ASCI_OHM} TruliooME Agent Core :: Searching for Global Gateway Account "
                  F"({account_name})..."
                  F" {ASCI_RESET}")
            account_name_row_element = element_forge.get_table_row_element_by_cell_value(
                table_row_elements=accountlist_table_rows, cell_index=0, target_text=search_value,)
            account_name_cell = element_forge.get_table_row_cell_element_by_cell_value(
                table_row_element=account_name_row_element, cell_index=0, target_text=search_value,)
            if account_name_cell.text.strip() == search_value:
                print(F"\t{ASCI_TEAL}{ASCI_OHM} TruliooME Agent Core :: Global Gateway Account "
                      F"({account_name}) found"
                      F"{ASCI_RESET}")
                account_link = account_name_cell.find_element(By.TAG_NAME, "a")
                account_link.click()
            elif account_name_cell.text.strip() != search_value:
                print(F"\t{ASCI_RED}{ASCI_OHM} TruliooME Agent Core :: Global Gateway Account ({account_name}) "
                      F"not found {ASCI_RESET}")
                is_complete = False
            if element_forge.page_title_is("AccountOverview"):
                is_complete = True
        return self.webdriver, is_complete

    async def create_global_gateway_account_test_entity(
            self, country: str, entity_name: str,
            entity_type: Optional[str] = "KYC", web_driver: Optional[WebDriver] = None) -> tuple[WebDriver, bool]:
        is_complete = False
        if web_driver is None:
            web_driver = self.webdriver
        element_forge = Prometheum(webdriver=web_driver)
        print(F"\t{ASCI_TEAL}{ASCI_OHM} TruliooME Agent Core :: Create Global Gateway {entity_type} "
              F"{Hermes.get_country_code(country)} Account Test Entity ({entity_name})"
              F" {ASCI_RESET}")
        if element_forge.page_title_is("AccountOverview"):
            test_entity_button = element_forge.get_element_by(
                locator_strategy=By.XPATH,
                locator_value="//a[normalize-space()='Test Entities']")
            if test_entity_button:
                test_entity_button.click()
                if element_forge.page_title_is("Test Entities"):
                    select_country_configuration = element_forge.get_element_by(
                        locator_strategy="xpath", locator_value='//*[@id="SelectedConfiguration"]')
                    country_select = element_forge.select_dropdown_option_webelement_by_text_value_index(
                        dropdown_webelement=select_country_configuration,
                        text=F"{Hermes.validate_country(country)}-Identity Verification")
                    view_test_entities_button = element_forge.get_element_by(
                        locator_strategy="xpath",
                        locator_value='//*[@id="content-header"]/table/tbody/tr/td/form/input[3]')
                    if country_select:
                        view_test_entities_button.click()
                        if element_forge.page_title_is("Test Entities"):
                            create_new_button = element_forge.get_element_by(
                                locator_strategy="xpath",
                                locator_value="//*[normalize-space()='Create New']")
                            if create_new_button:
                                create_new_button.click()
                                if element_forge.page_title_is("Create New Test Entity"):
                                    entity_name_field = element_forge.get_element_by(
                                        locator_strategy="xpath",
                                        locator_value='//*[@id="TestEntityName"]')
                                    if entity_name_field:
                                        entity_name_field.send_keys(entity_name)
                                        is_complete = True
        return web_driver, is_complete

    async def create_global_gateway_subaccount_test_entity(self, account_name: str,
                                                        account_identifier: Optional[str] = None,
                                                        web_driver: Optional[WebDriver] = None):
        pass



