import random
from datetime import timedelta
from typing import final

from hamcrest import is_ # type: ignore
import pytest
import tenacity
from python_selenium.terminalx_configuration import TerminalXConfiguration
from python_selenium.utils.logger import *
from python_selenium.testing.abstract_tests_base import *
from python_selenium.testing.exceptions import *
from python_selenium.testing.generic_steps import *


@logger
@final
class BddScenarioTests(AbstractTestsBase[GenericSteps[TerminalXConfiguration], TerminalXConfiguration]):
    _steps_type = GenericSteps

    def should_work(self):
        (self.steps
            .given.nothing
            .when.waiting(timedelta(seconds=1))
            .then.it_works(is_(True)))

    def should_fail(self):
        with pytest.raises(TestException):
            (self.steps
                .given.nothing
                .when.failing(TestException("just failing")))

    def should_swallow_exception(self):
        (self.steps
            .given.nothing
            .when.safely(lambda: self.steps.when.failing(TestException("boom")))
            .then.it_works(is_(True)))

    def should_retry(self):
        with pytest.raises(tenacity.RetryError):
            (self.steps
                .given.nothing
                .when.retrying(lambda: self.steps.when.failing(TestException("boom"))))

    def should_repeat(self):
        (self.steps
            .given.nothing
            .when.repeating(
                range(1, 4),
                lambda rep: self.steps.when.waiting(timedelta(seconds=rep)))
            .then.it_works(is_(True)))

    def should_eventually_work(self):
        def do_something_unreliable() -> str:
            if random.randint(0, 10) > 2:
                raise TestException("failed")
            else:
                return "ok"

        # NOTE the retries policy is defined in GenericSteps
        (self.steps
            .given.nothing
            .then.eventually_assert_that(
                lambda: do_something_unreliable(),
                is_("ok")))
