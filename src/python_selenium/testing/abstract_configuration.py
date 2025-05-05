import configparser
from abc import ABC
from functools import cached_property
from pathlib import Path
from typing import final

from python_selenium.utils.logger import LoggerMixin
from python_selenium.utils.object_utils import ImmutableMixin


class AbstractConfiguration(ABC, LoggerMixin, ImmutableMixin):
    """
    Base class for all types of configurations, providing a parser for a
    pre-specified configuration file.
    """
    _path: Path

    def __init__(self, path: Path):
        """
        Specifies the configuration file from which to read properties.

        Args:
            path (Path): relative path to configuration file

        Raises:
            FileNotFoundError: if the configuration file does not exit
        """
        if not path.exists():
            raise FileNotFoundError(path.absolute())

        self.log.debug(f"using configuration from {path}")
        self._path = path

    # NOTE if properties cannot be cached, this is a red-flag
    # configuration properties should be immutable.
    @final
    @cached_property
    def parser(self) -> configparser.ConfigParser:
        """
        Parser that reads this configuration.
        """
        self.log.debug(f"reading configuration from {self._path}")
        parser = configparser.ConfigParser()
        config_files = parser.read(self._path)
        self.log.debug(f"successfully read {config_files}")
        return parser
