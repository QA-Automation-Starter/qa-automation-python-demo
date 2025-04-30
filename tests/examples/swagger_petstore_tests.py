from hamcrest import is_  # type: ignore
from python_selenium.examples.swagger_petstore_configuration import SwaggerPetstoreConfiguration
from python_selenium.examples.swagger_petstore_steps import SwaggerPetstoreSteps
from python_selenium.model.examples.swagger_petstore_pet import SwaggerPetstorePet
from python_selenium.rest.rest_tests import RestTests
from python_selenium.utils.matchers import tracing_matcher, yields_item


class SwaggerPetstoreTests(
        RestTests[SwaggerPetstoreSteps, SwaggerPetstoreConfiguration]):
    _steps_type = SwaggerPetstoreSteps
    _configuration = SwaggerPetstoreConfiguration()

    def should_add(self):
        random_pet = SwaggerPetstorePet.random()
        (self.steps
            .given.configuration(self._configuration)
            .and_.swagger_petstore(self.rest_client)
            .when.adding(random_pet)
            .then.the_available_pets(yields_item(
                tracing_matcher(is_(random_pet)))))
