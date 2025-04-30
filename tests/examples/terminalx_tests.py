import random
from hamcrest import is_  # type: ignore
from python_selenium.model.examples.terminalx_user import TerminalXUser
from python_selenium.selenium.selenium_tests import SeleniumTests
from python_selenium.examples.terminalx_configuration import TerminalXConfiguration
from python_selenium.utils.matchers import contains_string_ignoring_case, tracing_matcher, yields_item
from python_selenium.examples.terminalx_steps import TerminalXSteps


class TerminalXTests(SeleniumTests[TerminalXSteps, TerminalXConfiguration]):
    _steps_type = TerminalXSteps
    _configuration = TerminalXConfiguration()

    def login_section(self, user: TerminalXUser):
        (self.steps
            .given.configuration(self._configuration)
            .and_.terminalx(self.web_driver)
            .when.logging_in_with(user.credentials)
            .then.the_user_logged_as(is_(user.name)))

    def should_login(self):
        self.login_section(random.choice(self._configuration.users))

    def should_find(self):
        self.login_section(random.choice(self._configuration.users))

        (self.steps
            .when.clicking_search())

        for word in ["hello", "kitty"]:
            (self.steps
                .when.searching_for(word)
                .then.the_search_hints(yields_item(tracing_matcher(contains_string_ignoring_case(word)))))
