from typing import Self
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from python_selenium.model.credentials import Credentials
from python_selenium.selenium.selenium_steps import Locator, SeleniumSteps
from python_selenium.test_configuration import TestConfiguration


class TerminalXSteps(SeleniumSteps[TestConfiguration]):
    def terminalx(self, driver: WebDriver) -> Self:
        self.web_driver = driver
        return self

    def clicking_login(self) -> Self:
        return self.clicking(lambda: self.element(
                    Locator(By.XPATH, "//div[contains(text(), 'התחברות')]")))

    def logging_in_with(self, credentials: Credentials) -> Self:
        return (self.clicking_login()
            .and_.typing(lambda: self.element(
                    Locator(By.ID, "qa-login-email-input")),
                credentials.username)
            .and_.typing(lambda: self.element(
                    Locator(By.ID, "qa-login-password-input")),
                credentials.username))

    def the_user_is_logged_in(self) -> Self:
        return self