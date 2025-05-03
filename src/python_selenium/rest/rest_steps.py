from enum import Enum
from typing import Self, final
from hamcrest import is_  # type: ignore
import requests

from requests import Request, Response

from python_selenium.testing.abstract_configuration import AbstractConfiguration
from python_selenium.testing.generic_steps import GenericSteps
from python_selenium.utils.logger import traced
from hamcrest.core.matcher import Matcher


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"

class RestSteps[TConfiguration: AbstractConfiguration](
    GenericSteps[TConfiguration]
):
    _rest_session: requests.Session

    @final
    def _invoke(self, request: Request) -> Response:
        return self._rest_session.send(
            self._rest_session.prepare_request(request))

    @traced
    @final
    def invoking(self, request: Request) -> Self:
        return self.eventually_assert_that(
            lambda: self._invoke(request).ok, is_(True))

    @traced
    @final
    def the_invocation(
            self, request: Request, by_rule: Matcher[Response]) -> Self:
        return self.eventually_assert_that(
            lambda: self._invoke(request),
            by_rule)
