# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from typing import Iterator, Self, final

from hamcrest.core.matcher import Matcher
from qa_pytest_webdriver import By, SeleniumSteps
from qa_testing_utils import Context, adapted_iterator, adapted_object
from selenium.webdriver.remote.webdriver import WebDriver

from qa_automation_python_demo.model.examples.terminalx_credentials import (
    TerminalXCredentials,
)
from qa_automation_python_demo.terminalx_configuration import (
    TerminalXConfiguration,
)


@final
class TerminalXSteps(SeleniumSteps[TerminalXConfiguration]):
    @Context.traced
    def terminalx(self, driver: WebDriver) -> Self:
        self._web_driver = driver
        self._web_driver.get(self.configured.landing_page)
        return self

    def clicking_login(self) -> Self:
        return self.clicking(By.xpath("//div[contains(text(), 'התחברות')]"))

    @Context.traced
    def clicking_search(self) -> Self:
        return self.clicking(
            By.xpath("//button[@data-test-id='qa-header-search-button']"))

    def submitting_login(self) -> Self:
        return self.clicking(By.xpath("//button[contains(text(), 'התחברות')]"))

    @Context.traced
    def logging_in_with(self, credentials: TerminalXCredentials) -> Self:
        return (self.clicking_login()
                .and_.typing(
                    By.id("qa-login-email-input"), credentials.username)
                .and_.typing(
                    By.id("qa-login-password-input"), credentials.password)
                .and_.submitting_login())

    @Context.traced
    def the_user_logged_in(self, by_rule: Matcher[str]) -> Self:
        return self.the_element(
            By.xpath(
                "//button[@data-test-id='qa-header-profile-button']/span[2]"),
            adapted_object(lambda element: element.text, by_rule))

    @Context.traced
    def searching_for(self, text: str) -> Self:
        return self.typing(
            By.xpath("//input[@data-test-id='qa-search-box-input']"),
            text)

    @Context.traced
    def the_search_hints(self, by_rule: Matcher[Iterator[str]]) -> Self:
        return self.the_elements(
            By.xpath("(//ul[@class='list_3tWy'])[2]/li/div/div/a"),
            adapted_iterator(lambda element: element.text, by_rule))
