# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from dataclasses import asdict
from typing import Iterator, Self, final

import requests
from hamcrest.core.matcher import Matcher
from qa_pytest_rest import HttpMethod, RestSteps
from qa_testing_utils import Context, adapted_object
from requests import Request

from qa_automation_python_demo.model.examples.swagger_petstore_pet import (
    SwaggerPetstorePet,
)
from qa_automation_python_demo.swagger_petstore_configuration import (
    SwaggerPetstoreConfiguration,
)


@final
class SwaggerPetstoreSteps(RestSteps[SwaggerPetstoreConfiguration]):

    @Context.traced
    def swagger_petstore(self, client: requests.Session):
        self._rest_session = client
        return self

    @Context.traced
    def adding(self, pet: SwaggerPetstorePet) -> Self:
        return self.invoking(Request(
            method=HttpMethod.POST,
            url=self.configured.resource_uri(path="pet"),
            json=asdict(pet)
        ))

    @Context.traced
    def the_available_pets(self, by_rule: Matcher
                           [Iterator[SwaggerPetstorePet]]) -> Self:
        return self.the_invocation(Request(
            method=HttpMethod.GET,
            url=self.configured.resource_uri(path="pet/findByStatus"),
            params={"status": "available"}),
            adapted_object(
                lambda response: SwaggerPetstorePet.from_(response),
                by_rule))
