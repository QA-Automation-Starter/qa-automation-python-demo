import pytest
from python_selenium.model.credentials import Credentials
from python_selenium.selenium.selenium_tests import SeleniumTests
from python_selenium.test_configuration import TestConfiguration
from tests.terminalx_steps import TerminalXSteps


class TerminalXTests(SeleniumTests[TerminalXSteps, TestConfiguration]):
    _steps_type = TerminalXSteps
    _configuration = TestConfiguration()


    @pytest.mark.parametrize("credentials", [
        Credentials(username="Checking2@percepti.co",password="Checking2@percepti.c"),
        Credentials(username="Checking@percepti.co",password="Checking@percepti.c1")
    ])
    def should_login(self, credentials: Credentials):
        (self.steps
            .given.terminalx(self.web_driver)
            .when.logging_in_with(credentials)
            .then.the_user_is_logged_in())