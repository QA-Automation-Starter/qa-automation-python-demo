from typing import override
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from python_selenium.selenium.selenium_steps import SeleniumSteps
from python_selenium.testing.abstract_configuration import AbstractConfiguration
from python_selenium.testing.abstract_tests_base import AbstractTestsBase


class SeleniumTests[TSteps:SeleniumSteps, TConfiguration: AbstractConfiguration](AbstractTestsBase[TSteps, TConfiguration]):
    web_driver: WebDriver

    @override
    def setup_method(self):
        super().setup_method()
        options = Options()
        options.add_argument("--start-maximized")

        self.web_driver = Chrome(
            options,
            Service(ChromeDriverManager().install()))

    @override
    def teardown_method(self):
        super().teardown_method()
        self.web_driver.quit()
