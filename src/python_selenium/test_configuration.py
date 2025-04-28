from pathlib import Path
from typing import final
from python_selenium.testing.abstract_configuration import AbstractConfiguration


class TestConfiguration(AbstractConfiguration):

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
