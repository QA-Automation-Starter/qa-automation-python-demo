# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from typing import override

from qa_pytest_webdriver.selenium_tests import SeleniumTests

from qa_automation_python_demo.amazon_configuration import AmazonConfiguration
from qa_automation_python_demo.amazon_steps import AmazonSteps


class AmazonTests(
    SeleniumTests[AmazonSteps[AmazonConfiguration],
                  AmazonConfiguration]):
    _steps_type = AmazonSteps
    _configuration = AmazonConfiguration()

    def should_checkout(self):
        '''
        Assumes delivery location was previously set to UK, otherwise Amazon
        does not ship to Israel, and adding to cart will be disabled.
        '''
        (self.steps
         .given.amazon(self.web_driver)
         .when.searching_for("mobile phone")  # mobile does not return phones
         .and_.selecting_result(2)  # 3rd result not always shown
         .and_.adding_to_cart()
         .and_.proceed_to_checkout()
         .then.signin_required())

    @override
    def setup_method(self) -> None:
        from selenium.webdriver import Firefox
        from selenium.webdriver.firefox.options import Options as FirefoxOptions
        from selenium.webdriver.firefox.service import Service as FirefoxService
        from webdriver_manager.firefox import GeckoDriverManager
        if self._configuration.parser.has_option("selenium", "browser_type") \
                and self._configuration.parser["selenium"]["browser_type"] == "firefox":
            # trigger with:
            # pytest --config selenium:browser_type=firefox tests/amazon_tests.py::AmazonTests
            options = FirefoxOptions()
            service = FirefoxService(GeckoDriverManager().install())
            self._web_driver = Firefox(options=options, service=service)
            self._web_driver.set_window_size(1920, 1080)  # type: ignore
        else:
            super().setup_method()
