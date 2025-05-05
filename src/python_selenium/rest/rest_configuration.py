from functools import cached_property
from typing import final
from urllib.parse import urljoin

from python_selenium.testing.abstract_configuration import AbstractConfiguration
from python_selenium.utils.string_utils import EMPTY


class RestConfiguration(AbstractConfiguration):

    @final
    @cached_property
    def endpoint_base(self) -> str:
        return self.parser["endpoint"]["base"]

    def endpoint_url(self, path: str = EMPTY) -> str:
        return urljoin(self.endpoint_base, path)
