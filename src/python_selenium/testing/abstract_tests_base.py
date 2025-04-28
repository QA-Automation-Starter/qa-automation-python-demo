from abc import ABC
from functools import cached_property
from typing import Any, Type, final

from python_selenium.testing.generic_steps import GenericSteps
from python_selenium.testing.abstract_configuration import AbstractConfiguration
from python_selenium.utils.logger import LoggerMixin
from python_selenium.utils.object_utils import ImmutableMixin


class AbstractTestsBase[TSteps:GenericSteps[Any], TConfiguration:AbstractConfiguration](
        ABC, LoggerMixin, ImmutableMixin):
    """
    Basic test scenario implementation, holding some type of steps and a logger
    facility.

    Subtypes must set `_steps_type` to the actual type of steps implementation::

                            +---------------+
                            |  BddKeyWords  |
                            +---------------+
                                            ^
                                            |
                                        implements
                                            |
        +-------------------+               +--------------+
        | AbstractTestsBase |---contains--->| GenericSteps |
        |                   |               +--------------+
        |                   |                       +-----------------------+
        |                   |---contains----------->| AbstractConfiguration |
        +-------------------+                       +-----------------------+

    Args:
        TSteps (TSteps:GenericSteps): The actual steps implementation, or partial implementation.
    """
    _steps_type: Type[TSteps]  # IMPORTANT: pytest classes must not __init__
    _configuration: TConfiguration

    @final
    @cached_property
    def steps(self) -> TSteps:
        '''
        Lazily initializes and returns an instance of steps implementation.

        Returns:
            TSteps: The instance of steps implementation.
        '''
        self.log.debug(f"initiating {self._steps_type}")
        return self._steps_type()

    def setup_method(self):
        """
        Override in subtypes with specific setup, if any.
        """
        self.log.debug("setup")

    def teardown_method(self):
        """
        Override in subtypes with specific teardown, if any.
        """
        self.log.debug("teardown")
