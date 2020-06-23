import enum
import os
from datetime import datetime

from selenium.common.exceptions import *
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select, WebDriverWait


def get_locator(locator_info):
    """
    Used to returned tuple with locator type and its value
    :param locator_info: list of locator type and its value
    :return: locator and its value as a tuple
    """
    locator_type = None
    locator_value = None
    for key, value in locator_info.items():
        locator_type = key
        locator_value = value
    return locator_type, locator_value


class LocatorType(enum.Enum):
    id = 1
    name = 2
    class_name = 3
    link_text = 4
    tag_name = 5
    partial_link_text = 6
    css = 7
    xpath = 8


class SeleniumWrapper:
    """
    Selenium wrapper class for all the built-in methods.
    """

    wait_time = 60
    driver = None

    def get_by_type(self, locator_type):
        """
        Gets the type from selenium By class.
        :param locator_type: type of locator.
        :return: By type of locator.
        """

        locator = {"id": By.ID,
                   "name": By.NAME,
                   "class_name": By.CLASS_NAME,
                   "link_text": By.LINK_TEXT,
                   "tag_name": By.TAG_NAME,
                   "partial_link_text": By.PARTIAL_LINK_TEXT,
                   "css": By.CSS_SELECTOR,
                   "xpath": By.XPATH
                   }

        if locator_type not in locator:
            raise AttributeError
        return locator[locator_type]

    def wait_for_page_load(self, timeout=wait_time):
        """
        Waits for document state to be ready.
        :return: none
        """

        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(lambda driver: self.driver.execute_script('return document.readyState === "complete"'))
        except TimeoutException as te:
            msg = "Exception occurred while loading the page"
            raise te

    def get_element(self, locator_info, timeout=wait_time):
        """
        To find the element in DOM to interact with.
        :param locator_info:  unique locator and locator type.
        :param timeout: wait time.
        :return: identified web element.
        """
        element = None

        self.wait_for_page_load()
        counter = 0
        attempts = 0
        if self.driver.name == "Safari":
            attempts = 1
        while counter <= attempts:
            element = self.wait_for_element_to_be_visible(locator_info, timeout, counter, attempts)
            if element:
                break
            counter += 1
        if element is None:
            raise NoSuchElementException
        return element

    def element_click(self, locator_info, timeout=wait_time):
        """
        To find the web element and clicking.
        :param locator_info: contains unique locator type and locator.
        :param timeout: wait time
        :return: none.
        """

        element_exists = self.is_element_present(locator_info)
        if element_exists is False:
            raise NoSuchElementException
        element = self.get_element(locator_info, timeout)
        self.scroll_element_to_view(element)
        self.wait_for_element_to_be_clickable(locator_info, timeout)
        element.click()

    def js_click(self, locator_info, timeout=wait_time):
        """
        To find the web element and clicking.
        :param locator_info: contains unique locator type and locator.
        :param timeout:  wait time
        :return: none.
        """

        try:
            element = self.wait_for_element_to_be_present(locator_info, timeout)
            if element:
                self.driver.execute_script("arguments[0].click();", element)
            else:
                raise NoSuchElementException
        except Exception as ex:
            raise ex

    def send_text(self, data, locator_info, timeout=wait_time):
        """
        To find the element and sending data to that element.
        :param data: data to be sent to the element.
        :param locator_info: contains unique locator type and locator.
        :param timeout:  wait time
        :return: none.
        """

        if not self.is_element_present(locator_info):
            raise NoSuchElementException
        element = self.get_element(locator_info, timeout)
        self.scroll_element_to_view(element)
        element.clear()
        element.send_keys(data)

    def is_element_present(self, locator_info, timeout=wait_time):
        """
        To verify whether the element is present on DOM.
        :param locator_info: contains unique locator type and locator.
        :param timeout: wait time.
        :return: bool
        """
        result = False
        try:
            self.get_element(locator_info, timeout)
            result = True
        except Exception as ex:
            print("Element is not present with " + str(locator_info))
        return result

    def wait_for_element_to_be_visible(self, locator_info, timeout=wait_time, limit=0, max_limit=0):
        """
        To wait for an element is present on the DOM of a page and visible.
        :param locator_info: contains unique locator type and locator.
        :param timeout: time to wait.
        :param limit: counter
        :param max_limit: max limit counter
        :return: web element
        """
        locator_type, locator_value = get_locator(locator_info)
        try:
            by_type = self.get_by_type(locator_type)
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(expected_conditions.visibility_of_element_located((by_type, locator_value)))
        except TimeoutException as te:
            # if limit and max_limit are same then exception will throw
            if limit == max_limit:
                raise te
        except WebDriverException as de:
            msg = "element is not displayed with " + str(locator_info)
            if limit == max_limit:
                raise de

    def wait_for_element_to_be_clickable(self, locator_info, timeout=wait_time):
        """
        To wait for an element to click  explicitly.
        :param locator_info:  contains unique locator type and locator.
        :param timeout: time to wait.
        :return: Web element
        """
        locator_type, locator_value = get_locator(locator_info)
        try:
            by_type = self.get_by_type(locator_type)
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(expected_conditions.element_to_be_clickable((by_type, locator_value)))
        except TimeoutException as te:
            raise te
        return element

    def scroll_element_to_view(self, element):
        """
        Scrolls web-element to middle of screen.
        :param self:
        :param element: web-element
        :return: none
        """
        try:
            scroll_element_to_middle = """var viewPortHeight = Math.max(document.documentElement.clientHeight,
            window.innerHeight || 0);
                                       var elementTop = arguments[0].getBoundingClientRect().top;
                                       window.scrollBy(0, elementTop-(viewPortHeight/2));
                                       """
            self.driver.execute_script(scroll_element_to_middle, element)
        except WebDriverException as ex:
            raise ex

    def wait_for_element_to_be_present(self, locator_info, timeout=wait_time):
        """
        To wait for an element is present on the DOM of a page.
        :param locator_info: contains unique locator type and locator..
        :param timeout: wait time.
        :return: Web element
        """
        locator_type, locator_value = get_locator(locator_info)
        try:
            by_type = self.get_by_type(locator_type)
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(expected_conditions.presence_of_element_located((by_type, locator_value)))
        except TimeoutException as te:
            raise te
        return element
