from python_selenium.selenium.selenium_steps import SeleniumSteps
from python_selenium.testing.abstract_configuration import AbstractConfiguration
from python_selenium.testing.abstract_tests_base import AbstractTestsBase


class SeleniumTests[TConfiguration: AbstractConfiguration](AbstractTestsBase[SeleniumSteps[TConfiguration], TConfiguration]):
    pass