from pathlib import Path
from typing import List, final
from python_selenium.model.examples.terminalx_credentials import TerminalXCredentials
from python_selenium.model.examples.terminalx_user import TerminalXUser
from python_selenium.testing.abstract_configuration import AbstractConfiguration


class TerminalXConfiguration(AbstractConfiguration):

    def __init__(self, path: Path = Path("resources/terminalx-default-config.ini")):
        """
        Initializes with specified `config.ini` file.

        Args:
            path (Path, optional): path to a `config.ini` file.\
                Defaults to Path("tests/python/scenarios/default-config.ini").
        """
        super().__init__(path)

    @property
    @final
    def ui_url(self) -> str:
        return self.parser["ui"]["url"]

    @property
    @final
    def users(self) -> List[TerminalXUser]:
        users_section = self.parser["users"]
        return [
            TerminalXUser(TerminalXCredentials.from_(username_password), name=key)
            for key, username_password in users_section.items()
        ]
