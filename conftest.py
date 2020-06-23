
import pytest
from selenium import webdriver

from selenium_wrapper import SeleniumWrapper


@pytest.fixture(autouse=True)
def setup(request):
    """
    :param request: initialize the driver object
    :param get_driver_factory: fixture to initialize the WebDriverFactory
    :return: driver instance
    """
    try:
        SeleniumWrapper.driver = webdriver.Chrome(executable_path="chromedriver.exe")
        SeleniumWrapper.driver.maximize_window()

        if request.cls is not None:
            request.cls.driver = SeleniumWrapper.driver
        yield SeleniumWrapper.driver

        # All cases except when 'debugging' arg is passed and close_browser=False

        SeleniumWrapper.driver.quit()
    except Exception as e:
        print(e)