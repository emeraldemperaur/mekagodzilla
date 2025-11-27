from typing import Optional, cast
import pandas
from pandas import DataFrame
from io import StringIO
from selenium.common import NoSuchElementException, TimeoutException, ElementNotSelectableException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxWebDriver

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from artisan.artisan import Artisan
from moneta.moneta import Moneta


class Prometheum:
    """
    Element Finder Object for locating HTML DOM elemnets with Selenium webdriver locator strategies and explicit wait

    Supported Strategies: 'id', 'class', 'name', 'css-selector', 'tag', 'linktext', 'partiallinktext', 'xpath'
    """

    def __init__(self, webdriver: WebDriver, rpa_objective: Optional[str] = F"RPA Process Demo - "
                                                                            F"{Artisan.get_timestamp()}"):
        self.webdriver = webdriver
        self.rpaserver_directory = Moneta.get_server_directory()
        self.rpa_objective = rpa_objective

    def get_element_by(self, locator_strategy: str, locator_value: str, timeout: Optional[int] = 13) -> WebElement:
        """
                Get webelements by Selenium webdriver strategies and explicit wait

                :param locator_strategy:id, class, name, css-selector, tag, linktext, partiallinktext, xpath
                :param locator_value:string
                :param timeout:int
                :return:WebElement
                """
        webelement = None
        try:
            wait_for_element = WebDriverWait(self.webdriver, timeout)
            match locator_strategy.lower():
                case "id":
                    webelement = wait_for_element.until(EC.element_to_be_clickable((By.ID, locator_value)))
                case "class":
                    webelement = wait_for_element.until(EC.element_to_be_clickable((By.CLASS_NAME, locator_value)))
                case "name":
                    webelement = wait_for_element.until(EC.element_to_be_clickable((By.NAME, locator_value)))
                case "css-selector":
                    webelement = wait_for_element.until(EC.element_to_be_clickable((By.CSS_SELECTOR, locator_value)))
                case "tag":
                    webelement = wait_for_element.until(EC.element_to_be_clickable((By.TAG_NAME, locator_value)))
                case "linktext":
                    webelement = wait_for_element.until(EC.element_to_be_clickable((By.LINK_TEXT, locator_value)))
                case "partialtext":
                    webelement = wait_for_element.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT,
                                                                                    locator_value)))
                case "xpath":
                    webelement = wait_for_element.until(EC.element_to_be_clickable((By.XPATH,
                                                                                    locator_value)))
                case _:  # Default case, similar to 'else'
                    webelement = wait_for_element.until(EC.element_to_be_clickable((By.CSS_SELECTOR, locator_value)))
            return webelement
        except (NoSuchElementException, TimeoutException, ElementNotSelectableException):
            return webelement

    def get_elements_by(self, locator_strategy: str, locator_value: str,
                        timeout: Optional[int] = 13) -> list[WebElement]:
        """
        Get webelements by Selenium webdriver strategies and explicit wait: 'id', 'class', 'name', 'css-selector',
        'tag', 'linktext', 'partiallinktext', 'xpath'
        :param locator_strategy:
        :param locator_value:
        :param timeout:
        :return:
        """
        webelements = []
        try:
            wait_for_element = WebDriverWait(self.webdriver, timeout)
            match locator_strategy.lower():
                case "id":
                    webelements = wait_for_element.until(
                        EC.visibility_of_all_elements_located((By.ID, locator_value)))
                case "class":
                    webelements = wait_for_element.until(
                        EC.visibility_of_all_elements_located((By.CLASS_NAME, locator_value)))
                case "name":
                    webelements = wait_for_element.until(
                        EC.visibility_of_all_elements_located((By.NAME, locator_value)))
                case "css-selector":
                    webelements = wait_for_element.until(
                        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, locator_value)))
                case "tag":
                    webelements = wait_for_element.until(
                        EC.visibility_of_all_elements_located((By.TAG_NAME, locator_value)))
                case "linktext":
                    webelements = wait_for_element.until(
                        EC.visibility_of_all_elements_located((By.LINK_TEXT, locator_value)))
                case "partiallinktext":
                    webelements = wait_for_element.until(
                        EC.visibility_of_all_elements_located((By.PARTIAL_LINK_TEXT, locator_value)))
                case "xpath":
                    webelements = wait_for_element.until(
                        EC.visibility_of_all_elements_located((By.XPATH, locator_value)))
                case _:  # Default case, similar to 'else'
                    webelements = wait_for_element.until(
                        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, locator_value)))
            return webelements
        except (NoSuchElementException, TimeoutException, ElementNotSelectableException):
            return webelements

    def page_title_is(self, title_name, timeout: Optional[int] = 13) -> bool:
        try:
            wait_until = WebDriverWait(self.webdriver, timeout)
            result = wait_until.until(EC.title_is(title_name))
        except (NoSuchElementException, TimeoutException, ElementNotSelectableException):
            return False
        return result

    def page_title_contains(self, title_name, timeout: Optional[int] = 13) -> bool:
        try:
            wait_until = WebDriverWait(self.webdriver, timeout)
            result = wait_until.until(EC.title_contains(title_name))
        except (NoSuchElementException, TimeoutException, ElementNotSelectableException):
            return False
        return result

    def capture_snapshot(self, rpa_objective_name: str, is_error: Optional[bool] = False) -> bool:
        project_folder = Moneta.get_server_project_directory(rpa_objective_name)
        error_note = ""
        if is_error:
            error_note = "ERROR"
        file_path = Moneta.get_server_project_filepath(file_name=F'{rpa_objective_name}'
                                                                 F'{error_note}_{Artisan.get_timestamp()}.png',
                                                       rpa_server_project_folder=project_folder)
        result = self.webdriver.save_screenshot(filename=F"{file_path}")
        return result

    def capture_fullscreen_snapshot(self,
                                    rpa_objective_name: str,
                                    is_error: Optional[bool] = False) -> tuple[WebDriver, bool]:
        project_folder = Moneta.get_server_project_directory(rpa_objective_name)
        error_note = ""
        if is_error:
            error_note = "ERROR"
        result = False
        file_path = Moneta.get_server_project_filepath(
            file_name=F'{rpa_objective_name}{error_note}_FS_{Artisan.get_timestamp()}.png',
            rpa_server_project_folder=project_folder)
        browser_name = self.webdriver.capabilities['browserName'].lower()
        if browser_name == 'chrome':
            # Chrome Fullscreen
            # Determine full height and width of the page using JavaScript
            original_window_size = self.webdriver.get_window_size()
            total_width = self.webdriver.execute_script("return document.body.parentNode.scrollWidth")
            total_height = self.webdriver.execute_script("return document.body.parentNode.scrollHeight")
            self.webdriver.set_window_size(total_width, total_height)
            result = self.webdriver.save_screenshot(filename=F"{file_path}")
            self.webdriver.set_window_size(original_window_size['width'], original_window_size['height'])
        elif browser_name == 'firefox':
            firefox_driver = cast(FirefoxWebDriver, self.webdriver)
            result = firefox_driver.get_full_page_screenshot_as_file(filename=F'{file_path}')
        return self.webdriver, result

    def capture_webelement_snapshot(self, webelement: WebElement,
                                    rpa_objective_name: str,
                                    is_error: Optional[bool] = False) -> tuple[WebDriver, bool]:
        project_folder = Moneta.get_server_project_directory(rpa_objective_name)
        error_note = ""
        if is_error:
            error_note = "ERROR"
        file_path = Moneta.get_server_project_filepath(file_name=F'{rpa_objective_name}'
                                                                 F'{error_note}_{Artisan.get_timestamp()}.png',
                                                       rpa_server_project_folder=project_folder)
        result = webelement.screenshot(filename=F"{file_path}")
        return self.webdriver, result

    def get_table_element_data(self,
                               locator_strategy: str,
                               locator_value: str,
                               output_as: Optional[str] = None,
                               timeout: Optional[int] = 23) -> None | DataFrame | list[dict] | dict | WebElement:
        output = None
        try:
            wait_for_element = WebDriverWait(self.webdriver, timeout)
            webelement = None
            match locator_strategy.lower():
                case "id":
                    webelement = wait_for_element.until(EC.element_to_be_clickable((By.ID, locator_value)))
                case "class":
                    webelement = wait_for_element.until(EC.element_to_be_clickable((By.CLASS_NAME, locator_value)))
                case "name":
                    webelement = wait_for_element.until(EC.element_to_be_clickable((By.NAME, locator_value)))
                case "css-selector":
                    webelement = wait_for_element.until(EC.element_to_be_clickable((By.CSS_SELECTOR, locator_value)))
                case "tag":
                    webelement = wait_for_element.until(EC.element_to_be_clickable((By.TAG_NAME, locator_value)))
                case "xpath":
                    webelement = wait_for_element.until(EC.element_to_be_clickable((By.XPATH,
                                                                                    locator_value)))
                case _:  # Default case, similar to 'else'
                    webelement = wait_for_element.until(EC.element_to_be_clickable((By.CSS_SELECTOR, locator_value)))
            if webelement.tag_name.lower() != "table":
                raise ValueError(F"{locator_strategy}:{locator_value} is not a table")
            table_html = webelement.get_attribute("outerHTML")
            # Pandas: parse HTML <table> into a DataFrame
            data_frames = pandas.read_html(StringIO(table_html))
            # Pandas dataframe list, convert to row Dict(s) object
            data_frame = data_frames[0]
            if output_as == "dataframe":
                output = data_frame
            if output_as == "listofdicts":
                output = data_frame.to_dict(orient='records')
            if output_as == "dictoflists":
                output = data_frame.to_dict(orient='list')
            if output_as == "webelement":
                output = webelement
            elif output_as is None:
                output = data_frame
            return output
        except (NoSuchElementException, TimeoutException, ElementNotSelectableException):
            return output

    def get_table_row_elements_data(self,
                                    table_webelement: WebElement,
                                    include_header: Optional[bool] = False,
                                    timeout: Optional[int] = 23) -> None | list[WebElement]:
        wait_for_element = WebDriverWait(self.webdriver, timeout)
        if table_webelement.tag_name.lower() != "table":
            raise ValueError(F"{table_webelement}: is not a table")
        if not include_header:
            table_body = wait_for_element.until(lambda d: table_webelement.find_element(By.TAG_NAME, "tbody"))
            table_row_elements = table_body.find_elements(By.TAG_NAME, "tr")
        else:
            table_row_elements = wait_for_element.until(lambda d: table_webelement.find_elements(By.TAG_NAME,
                                                                                                 "tr"))
        return table_row_elements

    def get_table_row_element_by_cell_value(self, table_row_elements: list[WebElement],
                                            cell_index: int, target_text: str,
                                            timeout: Optional[int] = 23) -> None | WebElement:
        wait_for_element = WebDriverWait(self.webdriver, timeout)
        for table_row_element in table_row_elements:
            cells = wait_for_element.until(lambda d: table_row_element.find_elements(By.XPATH, "./th | ./td"))
            if len(cells) > cell_index and cells[cell_index].text.strip() == target_text:
                return table_row_element
        return None

    def get_table_row_cell_element_by_cell_value(self, table_row_element: WebElement,
                                                 cell_index: int, target_text: str,
                                                 timeout: Optional[int] = 23) -> None | WebElement:
        wait_for_element = WebDriverWait(self.webdriver, timeout)
        row_cells = wait_for_element.until(lambda d: table_row_element.find_elements(By.XPATH, "./th | ./td"))
        if cell_index >= len(row_cells):
            return None
        cell = row_cells[cell_index]
        if cell.text.strip() == target_text:
            return cell
        return None

    def get_table_row_cell_element_data(self, table_row_webelement: WebElement,
                                        include_header: Optional[bool] = False,
                                        timeout: Optional[int] = 23) -> list[WebElement]:
        wait_for_element = WebDriverWait(self.webdriver, timeout)
        if table_row_webelement.tag_name.lower() != "tr":
            raise ValueError(F"{table_row_webelement}: is not a table row <tr>")
        if not include_header:
            cell_elements = wait_for_element.until(lambda d:
                                                   table_row_webelement.find_elements(By.TAG_NAME, "td"))
        else:
            cell_elements = wait_for_element.until(lambda d:
                                                   table_row_webelement.find_elements(By.XPATH, "./th | ./td"))
        return cell_elements

    def get_list_element_data(self, list_webelement: WebElement, timeout: Optional[int] = 23) -> list[str] | None:
        # check if html list element
        if list_webelement.tag_name.lower() not in ["ul", "ol", "dl", "dt"]:
            raise ValueError(F"{list_webelement} is not an ordered (ol) or unordered (ul) or description (dl) "
                             F"html list element")
        try:
            wait_for_element = WebDriverWait(self.webdriver, timeout)
            html_list_element = wait_for_element.until(EC.element_to_be_clickable(list_webelement))
            html_list_items = html_list_element.find_elements(By.TAG_NAME, "li")
            list_element_items = [list_item.text.strip() for list_item in html_list_items]
            return list_element_items
        except (NoSuchElementException, TimeoutException, ElementNotSelectableException):
            return None

    def get_list_item_webelement_by_text(self, list_webelement: WebElement,
                                         text: str, timeout: Optional[int] = 13) -> WebElement | None:
        # check if list element
        if list_webelement.tag_name.lower() not in ["ul", "ol", "dl", "dt"]:
            raise ValueError(F"{list_webelement} is not an ordered (ol) or unordered (ul) or description (dl) "
                             F"html list element")
        try:
            wait_for_element = WebDriverWait(self.webdriver, timeout)
            html_list_element = wait_for_element.until(EC.element_to_be_clickable(list_webelement))
            html_list_items = html_list_element.find_elements(By.TAG_NAME, "li")
            list_element_item = [list_item for list_item in html_list_items if list_item.text == text]
            return list_element_item[0]
        except (NoSuchElementException, TimeoutException, ElementNotSelectableException):
            return None

    def click_list_webelement_item_by_text(self, list_webelement: WebElement,
                                           text: str, timeout: Optional[int] = 13) -> WebElement | None:
        # check if list element
        if list_webelement.tag_name.lower() not in ["ul", "ol", "dl", "dt"]:
            raise ValueError(F"{list_webelement} is not an ordered (ol) or unordered (ul) or description (dl) "
                             F"html list element")
        try:
            wait_for_element = WebDriverWait(self.webdriver, timeout)
            html_list_element = wait_for_element.until(EC.element_to_be_clickable(list_webelement))
            html_list_items = html_list_element.find_elements(By.TAG_NAME, "li")
            list_element_item = [list_item for list_item in html_list_items if list_item.text == text]
            list_element_item[0].click()
        except (NoSuchElementException, TimeoutException, ElementNotSelectableException):
            return None

    def get_dropdown_webelement_data(self, dropdown_webelement: WebElement, output_as: Optional[str] = None,
                                     timeout: Optional[int] = 13) -> list[WebElement] | list[str] | None:
        wait_for_element = WebDriverWait(self.webdriver, timeout)
        output = None
        if dropdown_webelement.tag_name.lower() != "select":
            raise ValueError(F"{dropdown_webelement}: is not a dropdown element <select>")
        dropdown_webelement = Select(dropdown_webelement)
        dropdown_options = wait_for_element.until(lambda d: dropdown_webelement.options)
        if output_as == "webelement":
            output = dropdown_options
        if output_as == "listofdicts":
            options_list = []
            for dropdown_option in dropdown_webelement.options:
                {"text": dropdown_option.text.strip(), "value": dropdown_option.get_attribute("value")}
                options_list.append(dropdown_option)
            output = options_list
        if output_as == "listoftexts":
            output = [option.text.strip() for option in dropdown_webelement.options]
        elif output_as is None:
            output = dropdown_options
        return output

    def get_dropdown_option_webelement_by_text_value_index(self, dropdown_webelement: WebElement,
                                                           text: str, locator_strategy: Optional[str] = None,
                                                           timeout: Optional[int] = 13) -> WebElement | None:
        wait_for_element = WebDriverWait(self.webdriver, timeout)
        output = None
        dropdown_webelement = Select(dropdown_webelement)
        dropdown_options = wait_for_element.until(lambda d: dropdown_webelement.options)
        if locator_strategy == "value":
            for dropdown_option in dropdown_options:
                if dropdown_option.get_attribute("value") == text:
                    output = dropdown_option
                    break
        if locator_strategy == "index":
            if not text.isdigit():
                raise ValueError(F"{text} is not an integer")
            text = int(text)
            if text < 0 or text >= len(dropdown_options):
                return None
            output = dropdown_options[text]
        elif locator_strategy is None:
            for dropdown_option in dropdown_options:
                if dropdown_option.text.strip() == text.strip():
                    output = dropdown_option
                    break
        return output

    def select_dropdown_option_webelement_by_text_value_index(self, dropdown_webelement: WebElement,
                                                              text: str, locator_strategy: Optional[str] = None,
                                                              timeout: Optional[int] = 13) -> WebElement | None:
        wait_for_element = WebDriverWait(self.webdriver, timeout)
        output = None
        dropdown_webelement = Select(dropdown_webelement)
        dropdown_options = wait_for_element.until(lambda d: dropdown_webelement.options)
        if locator_strategy == "value":
            for dropdown_option in dropdown_options:
                if dropdown_option.get_attribute("value") == text:
                    output = dropdown_option
                    break
        if locator_strategy == "index":
            if not text.isdigit():
                raise ValueError(F"{text} is not an integer")
            text = int(text)
            if text < 0 or text >= len(dropdown_options):
                return None
            output = dropdown_options[text]
        elif locator_strategy is None:
            for dropdown_option in dropdown_options:
                if dropdown_option.text.strip() == text.strip():
                    output = dropdown_option
                    break
        if output:
            output.click()
        return output

    def get_button_dropdown_webelement_data(self, button_dropdown_webelement: WebElement) -> WebElement | None:
        pass

    def get_button_dropdown_item_webelement_by_text(self, button_dropdown_webelement: WebElement,
                                                    text: str, timeout: Optional[int] = 13) -> WebElement | None:
        pass

    def select_button_dropdown_item_webelement_by_text(self, button_dropdown_webelement: WebElement,
                                                       text: str, timeout: Optional[int] = 13) -> WebElement | None:
        pass

    @staticmethod
    async def get_webelement_by_id(element_id: str, web_driver: WebDriver, timeout: Optional[int] = 13) -> WebElement:
        wait_for_element = WebDriverWait(web_driver, timeout)
        webelement = wait_for_element.until(EC.visibility_of_element_located((By.ID, element_id)))
        return webelement

    @staticmethod
    async def get_clickable_webelement_by_id(element_id: str, web_driver: WebDriver,
                                             timeout: Optional[int] = 13) -> WebElement:
        wait_for_element = WebDriverWait(web_driver, timeout)
        webelement = wait_for_element.until(EC.element_to_be_clickable((By.ID, element_id)))
        return webelement

    @staticmethod
    async def get_clickable_webelements_by_id(element_id: str, web_driver: WebDriver,
                                              timeout: Optional[int] = 13) -> list[WebElement]:
        wait_for_element = WebDriverWait(web_driver, timeout)
        webelement = wait_for_element.until(EC.visibility_of_all_elements_located((By.ID, element_id)))
        return webelement

    @staticmethod
    async def get_webelement_by_class_name(element_class_name: str, web_driver: WebDriver,
                                           timeout: Optional[int] = 13) -> WebElement:
        wait_for_element = WebDriverWait(web_driver, timeout)
        webelement = wait_for_element.until(EC.visibility_of_element_located((By.CLASS_NAME, element_class_name)))
        return webelement

    @staticmethod
    async def get_clickable_webelement_by_class_name(element_class_name: str, web_driver: WebDriver,
                                                     timeout: Optional[int] = 13) -> WebElement:
        wait_for_element = WebDriverWait(web_driver, timeout)
        webelement = wait_for_element.until(EC.element_to_be_clickable((By.CLASS_NAME, element_class_name)))
        return webelement

    @staticmethod
    async def get_webelements_by_class_name(element_class_name: str, web_driver: WebDriver,
                                            timeout: Optional[int] = 13) -> list[WebElement]:
        wait_for_element = WebDriverWait(web_driver, timeout)
        webelements = wait_for_element.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, element_class_name)))
        return webelements

    @staticmethod
    async def get_webelement_by_css_selector(element_css_selector: str, web_driver: WebDriver,
                                             timeout: Optional[int] = 13) -> WebElement:
        wait_for_element = WebDriverWait(web_driver, timeout)
        webelement = wait_for_element.until(EC.visibility_of_element_located((By.CSS_SELECTOR, element_css_selector)))
        return webelement

    @staticmethod
    async def get_webelements_by_css_selector(element_css_selector: str, web_driver: WebDriver,
                                              timeout: Optional[int] = 13) -> list[WebElement]:
        wait_for_element = WebDriverWait(web_driver, timeout)
        webelements = wait_for_element.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, element_css_selector)))
        return webelements

    @staticmethod
    async def get_clickable_webelement_by_css_selector(element_css_selector: str, web_driver: WebDriver,
                                                       timeout: Optional[int] = 13) -> WebElement:
        wait_for_element = WebDriverWait(web_driver, timeout)
        webelement = wait_for_element.until(EC.element_to_be_clickable((By.CSS_SELECTOR, element_css_selector)))
        return webelement

    @staticmethod
    async def get_webelement_by_name(element_name: str, web_driver: WebDriver,
                                     timeout: Optional[int] = 13) -> WebElement:
        wait_for_element = WebDriverWait(web_driver, timeout)
        webelement = wait_for_element.until(EC.visibility_of_element_located((By.NAME, element_name)))
        return webelement

    @staticmethod
    async def get_clickable_webelement_by_name(element_name: str, web_driver: WebDriver,
                                               timeout: Optional[int] = 13) -> WebElement:
        wait_for_element = WebDriverWait(web_driver, timeout)
        webelement = wait_for_element.until(EC.element_to_be_clickable((By.NAME, element_name)))
        return webelement

    @staticmethod
    async def get_clickable_webelements_by_name(element_name: str, web_driver: WebDriver,
                                                timeout: Optional[int] = 13) -> list[WebElement]:
        wait_for_element = WebDriverWait(web_driver, timeout)
        webelements = wait_for_element.until(EC.visibility_of_all_elements_located((By.NAME, element_name)))
        return webelements

    @staticmethod
    async def get_webelement_by_html_tag(tag_name: str, web_driver: WebDriver,
                                         timeout: Optional[int] = 13) -> WebElement:
        wait_for_element = WebDriverWait(web_driver, timeout)
        webelement = wait_for_element.until(EC.visibility_of_element_located((By.TAG_NAME, tag_name)))
        return webelement

    @staticmethod
    async def get_webelements_by_html_tag(tag_name: str, web_driver: WebDriver,
                                          timeout: Optional[int] = 13) -> list[WebElement]:
        wait_for_element = WebDriverWait(web_driver, timeout)
        webelements = wait_for_element.until(EC.visibility_of_all_elements_located((By.TAG_NAME, tag_name)))
        return webelements

    @staticmethod
    async def get_clickable_webelement_by_html_tag(tag_name: str, web_driver: WebDriver,
                                                   timeout: Optional[int] = 13) -> WebElement:
        wait_for_element = WebDriverWait(web_driver, timeout)
        webelement = wait_for_element.until(EC.element_to_be_clickable((By.TAG_NAME, tag_name)))
        return webelement

    @staticmethod
    async def get_webelement_by_link_text(link_text: str, web_driver: WebDriver,
                                          timeout: Optional[int] = 13) -> WebElement:
        wait_for_element = WebDriverWait(web_driver, timeout)
        webelement = wait_for_element.until(EC.visibility_of_element_located((By.LINK_TEXT, link_text)))
        return webelement

    @staticmethod
    async def get_clickable_webelement_by_link_text(link_text: str, web_driver: WebDriver,
                                                    timeout: Optional[int] = 13) -> WebElement:
        wait_for_element = WebDriverWait(web_driver, timeout)
        webelement = wait_for_element.until(EC.element_to_be_clickable((By.LINK_TEXT, link_text)))
        return webelement

    @staticmethod
    async def get_webelement_by_partial_link_text(link_text: str, web_driver: WebDriver,
                                                  timeout: Optional[int] = 13) -> WebElement:
        wait_for_element = WebDriverWait(web_driver, timeout)
        webelement = wait_for_element.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, link_text)))
        return webelement

    @staticmethod
    async def get_clickable_webelement_by_partial_link_text(link_text: str, web_driver: WebDriver,
                                                            timeout: Optional[int] = 13) -> WebElement:
        wait_for_element = WebDriverWait(web_driver, timeout)
        webelement = wait_for_element.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, link_text)))
        return webelement

    @staticmethod
    async def get_webelement_by_xpath(xpath: str, web_driver: WebDriver,
                                      timeout: Optional[int] = 13) -> WebElement:
        wait_for_element = WebDriverWait(web_driver, timeout)
        webelement = wait_for_element.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        return webelement

    @staticmethod
    async def get_clickable_webelement_by_xpath(xpath: str, web_driver: WebDriver,
                                                timeout: Optional[int] = 13) -> WebElement:
        wait_for_element = WebDriverWait(web_driver, timeout)
        webelement = wait_for_element.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return webelement
