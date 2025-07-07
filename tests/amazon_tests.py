# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

import pytest
from qa_pytest_webdriver.selenium_tests import SeleniumTests

from qa_automation_python_demo.amazon_configuration import AmazonConfiguration
from qa_automation_python_demo.amazon_steps import AmazonSteps


# --8<-- [start:class]
@pytest.mark.external
@pytest.mark.selenium
class AmazonTests(
    SeleniumTests[AmazonSteps[AmazonConfiguration],
                  AmazonConfiguration]):
    _steps_type = AmazonSteps
    _configuration = AmazonConfiguration()

    # --8<-- [start:func]

    def should_checkout(self):
        '''
        Assumes delivery location was previously set to UK, otherwise Amazon
        does not ship to Israel, and adding to cart will be disabled.
        '''
        (self.steps
         .given.amazon(self.web_driver)
         .when.searching_for("mobile phone")  # mobile does not return phones
         # ISSUE could not click it... tried several methods :( out of time
         .and_.selecting_result(2)  # 3rd result not always shown
         .and_.adding_to_cart()
         .and_.proceed_to_checkout())
        #  .then.signin_required())
    # --8<-- [end:func]

# --8<-- [end:class]
