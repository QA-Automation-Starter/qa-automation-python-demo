from dataclasses import asdict
from typing import Iterator, Self, final

from requests import Request
from hamcrest.core.matcher import Matcher
import requests

from python_selenium.examples.swagger_petstore_configuration import SwaggerPetstoreConfiguration
from python_selenium.model.examples.swagger_petstore_pet import SwaggerPetstorePet
from python_selenium.rest.rest_steps import RestSteps
from python_selenium.utils.logger import traced
from python_selenium.utils.matchers import adapted_object


@final
class SwaggerPetstoreSteps(RestSteps[SwaggerPetstoreConfiguration]):

    def swagger_petstore(self, client: requests.Session):
        self.rest_client = client
        return self

    @traced
    def adding(self, pet: SwaggerPetstorePet) -> Self:
        return self.invoking(Request(
            method="POST",
            # or passed in as an argument
            url=f"{self.configured.endpoint_url}/pet",
            json=asdict(pet)
        ))

    @traced
    def the_available_pets(self, by_rule: Matcher[Iterator[SwaggerPetstorePet]]) -> Self:
        return self.the_invocation(Request(
            method="GET",
            url=f"{self.configured.endpoint_url}/pet/findByStatus",
            params={"status": "available"}),
            adapted_object(
                lambda response: SwaggerPetstorePet.from_(response),
                by_rule))
