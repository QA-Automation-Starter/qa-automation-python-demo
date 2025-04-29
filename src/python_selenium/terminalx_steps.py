from typing import Iterator, Self, final
from hamcrest.core.matcher import Matcher
from selenium.webdriver.remote.webdriver import WebDriver
from python_selenium.model.credentials import Credentials
from python_selenium.selenium.selenium_steps import SeleniumSteps, By
from python_selenium.terminalx_configuration import TerminalXConfiguration
from python_selenium.utils.logger import traced


@final
class TerminalXSteps(SeleniumSteps[TerminalXConfiguration]):
    def terminalx(self, driver: WebDriver) -> Self:
        self.web_driver = driver
        self.web_driver.get(self.configured.ui_url)
        return self

    def clicking_login(self) -> Self:
        return self.clicking(By.xpath("//div[contains(text(), 'התחברות')]"))

    def clicking_search(self) -> Self:
        return self.clicking(By.xpath("//button[@data-test-id='qa-header-search-button']"))

    def submitting_login(self) -> Self:
        return self.clicking(By.xpath("//button[contains(text(), 'התחברות')]"))

    @traced
    def logging_in_with(self, credentials: Credentials) -> Self:
        return (self.clicking_login()
            .and_.typing(By.id("qa-login-email-input"), credentials.username)
            .and_.typing(By.id("qa-login-password-input"), credentials.password)
            .and_.submitting_login())

    @traced
    def the_user_logged_as(self, by_rule: Matcher[str]) -> Self:
        return self.eventually_assert_that(lambda: self.element(
                    By.xpath("//button[@data-test-id='qa-header-profile-button']/span[2]")).text,
                    by_rule)

    @traced
    def searching_for(self, text: str) -> Self:
        return self.typing(By.xpath("//input[@data-test-id='qa-search-box-input']"), text)

    @traced
    def the_search_hints(self, by_rule: Matcher[Iterator[str]]) -> Self:
        return self.eventually_assert_that(lambda: (
                element.text for element in self.elements(
                        By.xpath("(//ul[@class='list_3tWy'])[2]/li/div/div/a"))),
                    by_rule)