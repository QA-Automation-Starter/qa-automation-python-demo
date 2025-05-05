# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path
from typing import List, final
from python_selenium.model.examples.terminalx_credentials import TerminalXCredentials
from python_selenium.model.examples.terminalx_user import TerminalXUser
from python_selenium.selenium.selenium_configuration import SeleniumConfiguration


class TerminalXConfiguration(SeleniumConfiguration):

    def __init__(
            self, path: Path = Path("resources/terminalx-default-config.ini")):
        super().__init__(path)

    @property
    @final
    def users(self) -> List[TerminalXUser]:
        users_section = self.parser["users"]
        return [
            TerminalXUser(TerminalXCredentials.from_(username_password), name=key)
            for key, username_password in users_section.items()
        ]
