from typing import Self
from hamcrest.core.matcher import Matcher
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from python_selenium.model.credentials import Credentials
from python_selenium.selenium.selenium_steps import Locator, SeleniumSteps
from python_selenium.test_configuration import TestConfiguration


class TerminalXSteps(SeleniumSteps[TestConfiguration]):
    def terminalx(self, driver: WebDriver) -> Self:
        self.web_driver = driver
        self.web_driver.get(self.configured.ui_url)
        return self

    def clicking_login(self) -> Self:
        return self.clicking(lambda: self.element(
                    Locator(By.XPATH, "//div[contains(text(), 'התחברות')]")))

    def submitting_login(self) -> Self:
        return self.clicking(lambda: self.element(
                    Locator(By.XPATH, "//button[contains(text(), 'התחברות')]")))

    def logging_in_with(self, credentials: Credentials) -> Self:
        return (self.clicking_login()
            .and_.typing(lambda: self.element(
                    Locator(By.ID, "qa-login-email-input")),
                credentials.username)
            .and_.typing(lambda: self.element(
                    Locator(By.ID, "qa-login-password-input")),
                credentials.password)
            .and_.submitting_login())

    def the_user_is_logged_in(self, by_rule: Matcher[str]) -> Self:
        return self.eventually_assert_that(lambda: self.element(
                    Locator(By.XPATH,"//button[@data-test-id='qa-header-profile-button']/span[2]"))
                        .text,
                    by_rule)