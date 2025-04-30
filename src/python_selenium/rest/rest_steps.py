from typing import Self
from hamcrest import is_  # type: ignore
import requests

from requests import Request, Response

from python_selenium.testing.abstract_configuration import AbstractConfiguration
from python_selenium.testing.generic_steps import GenericSteps
from python_selenium.utils.logger import traced
from hamcrest.core.matcher import Matcher


class RestSteps[TConfiguration: AbstractConfiguration](
    GenericSteps[TConfiguration]
):
    rest_client: requests.Session

    def _invoke(self, request: Request) -> Response:
        return self.rest_client.send(self.rest_client.prepare_request(request))

    @traced
    def invoking(self, request: Request) -> Self:
        return self.eventually_assert_that(
            lambda: self._invoke(request).ok, is_(True))

    @traced
    def the_invocation(
            self, request: Request, by_rule: Matcher[Response]) -> Self:
        return self.eventually_assert_that(
            lambda: self._invoke(request),
            by_rule)
