# Trulioo SME Form(s) Interaction Logic
from typing import Optional
from selenium.webdriver.remote.webdriver import WebDriver

from artisan.virgil import Virgil
from artisan.virgil_kyb import VirgilKYB
from artisan.virgil_kyc import VirgilKYC
from heimdall.heimdall import Heimdall
from mercurius.http_models_testentity import GlobalGatewayCreateAccountTestEntityRPARequest, \
    GlobalGatewayCreateKYCSubAccountTestEntityRPARequest, GlobalGatewayCreateKYBSubAccountTestEntityRPARequest
from prometheus.prometheus_forge import Prometheum

class TruliooMEFormX:
    def __init__(self, webdriver: WebDriver,
                 rpa_objective: str, heimdall: Optional[Heimdall] = None) -> None:
        self.webdriver = webdriver
        self.heimdall = heimdall
        self.element_forge = Prometheum(webdriver=webdriver, rpa_objective=rpa_objective)

    async def fill_account_test_entity_form(self,
                                            country_name: str,
                                            parameters: GlobalGatewayCreateAccountTestEntityRPARequest
                                            ) -> tuple[WebDriver, bool]:
        rpa_webdriver = self.webdriver
        element_forge = self.element_forge
        on_form = False
        country_xpath_field_map = Virgil(country_name=country_name).get_account_entity_form_field_xpath_map()
        if element_forge.page_title_is(title_name="Create New Test Entity"):
            on_form = True
        if country_name in ["United States", "Canada"]:
            if on_form:
                first_name_field = element_forge.get_element_by(locator_strategy="xpath",
                                                                locator_value=country_xpath_field_map['first_name'])
                last_name_field = element_forge.get_element_by(locator_strategy="xpath",
                                                               locator_value=country_xpath_field_map['last_name'])
                address_1_field = element_forge.get_element_by(locator_strategy="xpath",
                                                               locator_value=country_xpath_field_map['address_1'])
                first_name_field.send_keys(parameters.first_name)
                last_name_field.send_keys(parameters.last_name)
                address_1_field.send_keys(parameters.address_1)
        return rpa_webdriver, True

    async def fill_kyc_subaccount_test_entity_form(self,
                                               country_name: str,
                                               parameters: GlobalGatewayCreateKYCSubAccountTestEntityRPARequest,
                                               entity_type: Optional[str] = "KYC") -> tuple[WebDriver, bool]:
        rpa_webdriver = self.webdriver
        element_forge = self.element_forge
        country_xpath_field_map = VirgilKYC(country_name=country_name).get_subaccount_entity_form_field_xpath_map()
        on_form = False
        if element_forge.page_title_is(title_name="Create New Test Entity"):
            on_form = True
        if country_name in ["United States", "Canada"]:
            if on_form:
                first_name_field = element_forge.get_element_by(locator_strategy="xpath",
                                                                locator_value=country_xpath_field_map['first_name'])
                last_name_field = element_forge.get_element_by(locator_strategy="xpath",
                                                               locator_value=country_xpath_field_map['last_name'])
                dob_day_field = element_forge.get_element_by(locator_strategy="xpath",
                                                             locator_value=country_xpath_field_map['date_of_birth_day'])
                dob_month_field = element_forge.get_element_by(
                    locator_strategy="xpath",
                    locator_value=country_xpath_field_map['date_of_birth_month'])
                dob_year_field = element_forge.get_element_by(locator_strategy="xpath",
                                                              locator_value=country_xpath_field_map['date_of_birth_year'])
                address_1_field = element_forge.get_element_by(locator_strategy="xpath",
                                                               locator_value=country_xpath_field_map['address_1'])
                first_name_field.send_keys(parameters.first_name)
                last_name_field.send_keys(parameters.last_name)
                dob_day_field.send_keys(parameters.date_of_birth_day)
                dob_month_field.send_keys(parameters.date_of_birth_month)
                dob_year_field.send_keys(parameters.date_of_birth_year)
                address_1_field.send_keys(parameters.address_1)
        return rpa_webdriver, True

    async def fill_kyb_subaccount_test_entity_form(self,
                                               country_name: str,
                                               parameters: GlobalGatewayCreateKYBSubAccountTestEntityRPARequest,
                                               entity_type: Optional[str] = "KYC") -> tuple[WebDriver, bool]:
        rpa_webdriver = self.webdriver
        element_forge = self.element_forge
        country_xpath_field_map = VirgilKYB(country_name=country_name).get_subaccount_entity_form_field_xpath_map()
        on_form = False
        if element_forge.page_title_is(title_name="Create New Test Entity"):
            on_form = True
        if country_name in ["United States", "Canada"]:
            if on_form:
                business_name_field = element_forge.get_element_by(locator_strategy="xpath",
                                                                   locator_value=country_xpath_field_map[
                                                                       'business_name'])
                address_1_field = element_forge.get_element_by(locator_strategy="xpath",
                                                               locator_value=country_xpath_field_map['address_1'])
                business_name_field.send_keys(parameters.business_name)
                address_1_field.send_keys(parameters.address_1)
        return rpa_webdriver, True

