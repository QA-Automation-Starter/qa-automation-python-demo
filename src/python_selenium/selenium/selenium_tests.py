from typing import Any, Generic, TypeVar, override
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from python_selenium.selenium.selenium_steps import SeleniumSteps
from python_selenium.testing.abstract_configuration import AbstractConfiguration
from python_selenium.testing.abstract_tests_base import AbstractTestsBase

# NOTE: python limitation; we cannot declare it such as:
# class SeleniumTests[TSteps:SeleniumSteps[TConfiguration], TConfiguration: AbstractConfiguration](AbstractTestsBase[TSteps, TConfiguration]):
TConfiguration = TypeVar("TConfiguration", bound=AbstractConfiguration)
TSteps = TypeVar("TSteps", bound=SeleniumSteps[Any])


class SeleniumTests(Generic[TSteps, TConfiguration], AbstractTestsBase[TSteps, TConfiguration]):
    web_driver: WebDriver

    @override
    def setup_method(self):
        super().setup_method()
        options = Options()
        options.add_argument("--start-maximized")  # type: ignore

        self.web_driver = Chrome(
            options,
            Service(ChromeDriverManager().install()))

    @override
    def teardown_method(self):
        super().teardown_method()
        self.web_driver.quit()
