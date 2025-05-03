from pathlib import Path
from typing import final
from urllib.parse import urljoin
from python_selenium.testing.abstract_configuration import AbstractConfiguration
from python_selenium.utils.string_utils import EMPTY


class SwaggerPetstoreConfiguration(AbstractConfiguration):

    def __init__(
            self,
            path: Path = Path("resources/swagger-petstore-default-config.ini")):
        """
        Initializes with specified `config.ini` file.

        Args:
            path (Path, optional): path to a `config.ini` file.\
                Defaults to Path("tests/python/scenarios/default-config.ini").
        """
        super().__init__(path)

    @final
    @property
    def endpoint_base(self) -> str:
        return self.parser["endpoint"]["base"]

    @final
    def endpoint_url(self, path: str = EMPTY) -> str:
        return urljoin(self.endpoint_base, path)
