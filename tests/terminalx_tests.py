import random
from hamcrest import is_ # type: ignore
from python_selenium.selenium.selenium_tests import SeleniumTests
from python_selenium.test_configuration import TestConfiguration
from tests.terminalx_steps import TerminalXSteps


class TerminalXTests(SeleniumTests[TerminalXSteps, TestConfiguration]):
    _steps_type = TerminalXSteps
    _configuration = TestConfiguration()


    def should_login(self):
        user = random.choice(self._configuration.users)

        (self.steps
            .given.configuration(self._configuration)
            .and_.terminalx(self.web_driver)
            .when.logging_in_with(user.credentials)
            .then.the_user_is_logged_in(is_(user.name)))