# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from typing import List, final

from qa_pytest_webdriver import SeleniumConfiguration

from qa_automation_python_demo.model.examples.terminalx_credentials import (
    TerminalXCredentials,
)
from qa_automation_python_demo.model.examples.terminalx_user import (
    TerminalXUser,
)


class TerminalXConfiguration(SeleniumConfiguration):

    @property
    @final
    def users(self) -> List[TerminalXUser]:
        users_section = self.parser["users"]
        return [
            TerminalXUser(TerminalXCredentials.from_(username_password), name=key)
            for key, username_password in users_section.items()
        ]
