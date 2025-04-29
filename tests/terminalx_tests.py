import random
from hamcrest import contains, contains_string, is_ # type: ignore
from python_selenium.model.user import User
from python_selenium.selenium.selenium_tests import SeleniumTests
from python_selenium.test_configuration import TestConfiguration
from python_selenium.utils.matchers import yields_item
from tests.terminalx_steps import TerminalXSteps


class TerminalXTests(SeleniumTests[TerminalXSteps, TestConfiguration]):
    _steps_type = TerminalXSteps
    _configuration = TestConfiguration()

    def login_section(self, user: User):
        (self.steps
            .given.configuration(self._configuration)
            .and_.terminalx(self.web_driver)
            .when.logging_in_with(user.credentials)
            .then.the_user_is_logged_in(is_(user.name)))


    def should_login(self):
        self.login_section(random.choice(self._configuration.users))

    def should_find(self):
        self.login_section(random.choice(self._configuration.users))

        (self.steps
            .given.configuration(self._configuration)
            .and_.terminalx(self.web_driver)
            .when.searching_for("hello")
            .then.the_search_hints(yields_item(contains_string("Hello"))))
