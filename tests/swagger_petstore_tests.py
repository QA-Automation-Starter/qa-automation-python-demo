# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from hamcrest import is_  # type: ignore
from qa_automation_python_demo.swagger_petstore_configuration import SwaggerPetstoreConfiguration
from qa_automation_python_demo.swagger_petstore_steps import SwaggerPetstoreSteps
from qa_automation_python_demo.model.examples.swagger_petstore_pet import SwaggerPetstorePet
from qa_pytest_rest.rest_tests import RestTests
from qa_testing_utils.matchers import traced, yields_item


class SwaggerPetstoreTests(
        RestTests[SwaggerPetstoreSteps, SwaggerPetstoreConfiguration]):
    _steps_type = SwaggerPetstoreSteps
    _configuration = SwaggerPetstoreConfiguration()

    def should_add(self):
        random_pet = SwaggerPetstorePet.random()
        (self.steps
            .given.swagger_petstore(self._rest_session)
            .when.adding(random_pet)
            .then.the_available_pets(yields_item(traced(is_(random_pet)))))
