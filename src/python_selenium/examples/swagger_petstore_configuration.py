from pathlib import Path
from typing import final
from python_selenium.testing.abstract_configuration import AbstractConfiguration


class SwaggerPetstoreConfiguration(AbstractConfiguration):

    def __init__(self, path: Path = Path("resources/swagger-petstore-default-config.ini")):
        """
        Initializes with specified `config.ini` file.

        Args:
            path (Path, optional): path to a `config.ini` file.\
                Defaults to Path("tests/python/scenarios/default-config.ini").
        """
        super().__init__(path)

    @property
    @final
    def endpoint_url(self) -> str:
        return self.parser["endpoint"]["url"]
