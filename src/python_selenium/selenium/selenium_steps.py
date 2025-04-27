from python_selenium.testing.abstract_configuration import AbstractConfiguration
from python_selenium.testing.generic_steps import GenericSteps


class SeleniumSteps[TConfiguration:AbstractConfiguration](GenericSteps[TConfiguration]):
    pass