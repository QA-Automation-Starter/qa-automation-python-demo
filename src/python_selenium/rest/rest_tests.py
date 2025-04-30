from typing import Any, Generic, TypeVar, override

from python_selenium.rest.rest_steps import RestSteps
from python_selenium.testing.abstract_configuration import AbstractConfiguration
from python_selenium.testing.abstract_tests_base import AbstractTestsBase
import requests

# NOTE: python limitation; we cannot declare it such as:
# class SeleniumTests[TSteps:SeleniumSteps[TConfiguration], TConfiguration: AbstractConfiguration](AbstractTestsBase[TSteps, TConfiguration]):
TConfiguration = TypeVar("TConfiguration", bound=AbstractConfiguration)
TSteps = TypeVar("TSteps", bound=RestSteps[Any])


class RestTests(
        Generic[TSteps, TConfiguration],
        AbstractTestsBase[TSteps, TConfiguration]):
    rest_client: requests.Session

    @override
    def setup_method(self):
        super().setup_method()
        self.rest_client = requests.Session()

    @override
    def teardown_method(self):
        try:
            self.rest_client.close()
        finally:
            super().teardown_method()
