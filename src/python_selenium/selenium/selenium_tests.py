from typing import Any, Generic, TypeVar, override
from selenium.webdriver.remote.webdriver import WebDriver

from python_selenium.selenium.selenium_configuration import SeleniumConfiguration
from python_selenium.selenium.selenium_steps import SeleniumSteps
from python_selenium.testing.abstract_tests_base import AbstractTestsBase

# NOTE: python limitation; we cannot declare it such as:
# class SeleniumTests[TSteps:SeleniumSteps[TConfiguration], TConfiguration: AbstractConfiguration](AbstractTestsBase[TSteps, TConfiguration]):
TConfiguration = TypeVar("TConfiguration", bound=SeleniumConfiguration)
TSteps = TypeVar("TSteps", bound=SeleniumSteps[Any])


class SeleniumTests(
        Generic[TSteps, TConfiguration],
        AbstractTestsBase[TSteps, TConfiguration]):
    _web_driver: WebDriver

    @override
    def setup_method(self):
        super().setup_method()
        self._web_driver = self._configuration.web_driver

    @override
    def teardown_method(self):
        try:
            self._web_driver.quit()
        finally:
            super().teardown_method()
