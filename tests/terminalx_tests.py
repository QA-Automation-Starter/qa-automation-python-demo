import pytest
from hamcrest import is_ # type: ignore
from python_selenium.model.credentials import Credentials
from python_selenium.model.user import User
from python_selenium.selenium.selenium_tests import SeleniumTests
from python_selenium.test_configuration import TestConfiguration
from tests.terminalx_steps import TerminalXSteps


class TerminalXTests(SeleniumTests[TerminalXSteps, TestConfiguration]):
    _steps_type = TerminalXSteps
    _configuration = TestConfiguration()


    @pytest.mark.parametrize("user", [
        User(Credentials(username="Checking2@percepti.co",password="Checking2@percepti.c"), name="checker"),
        User(Credentials(username="Checking@percepti.co",password="Checking@percepti.c1"), name="per")
    ])
    def should_login(self, user: User):
        (self.steps
            .given.configuration(self._configuration)
            .and_.terminalx(self.web_driver)
            .when.logging_in_with(user.credentials)
            .then.the_user_is_logged_in(is_(user.name)))