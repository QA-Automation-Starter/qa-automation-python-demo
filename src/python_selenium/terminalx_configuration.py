from pathlib import Path
from typing import List, final
from python_selenium.model.credentials import Credentials
from python_selenium.model.user import User
from python_selenium.testing.abstract_configuration import AbstractConfiguration


class TerminalXConfiguration(AbstractConfiguration):

    def __init__(self, path: Path = Path("tests/resources/default-config.ini")):
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
    def users(self) -> List[User]:
        users_section = self.parser["users"]
        return [
            User(Credentials.from_(username_password), name=key)
            for key, username_password in users_section.items()
        ]
