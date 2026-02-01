# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

import random

from hamcrest import is_  # type: ignore
from qa_pytest_webdriver import SeleniumTests
from qa_testing_utils import contains_string_ignoring_case, tracing, yields_item

from qa_automation_python_demo.model.examples.terminalx_user import (
    TerminalXUser,
)
from qa_automation_python_demo.terminalx_configuration import (
    TerminalXConfiguration,
)
from qa_automation_python_demo.terminalx_steps import TerminalXSteps


class TerminalXTests(SeleniumTests[TerminalXSteps, TerminalXConfiguration]):
    _steps_type = TerminalXSteps
    _configuration = TerminalXConfiguration()

    # NOTE sections may be further collected in superclasses and reused across tests
    def login_section(self, user: TerminalXUser) -> TerminalXSteps:
        return (self.steps
                .given.terminalx(self.ui_context)
                .when.logging_in_with(user.credentials)
                .then.the_user_logged_in(is_(user.name)))

    def should_login(self):
        self.login_section(random.choice(self._configuration.users))

    def should_find(self):
        (self.login_section(random.choice(self._configuration.users))
            .when.clicking_search())

        for word in ["hello", "kitty"]:
            (self.steps
             .when.searching_for(word)
             .then.the_search_hints(yields_item(tracing(
                 contains_string_ignoring_case(word)))))

        for word in ["hello", "kitty"]:
            (self.steps
             .when.searching_for(word)
             .then.the_search_hints(yields_item(tracing(
                 contains_string_ignoring_case(word)))))
