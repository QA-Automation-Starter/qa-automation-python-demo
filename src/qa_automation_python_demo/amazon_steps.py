# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from typing import Self

from hamcrest.core import is_  # type: ignore
from qa_pytest_webdriver.selenium_steps import By, SeleniumSteps
from qa_testing_utils.logger import Context
from qa_testing_utils.matchers import adapted_object
from selenium.webdriver.remote.webdriver import WebDriver

from qa_automation_python_demo.amazon_configuration import AmazonConfiguration


class AmazonSteps[TConfiguration: AmazonConfiguration](
        SeleniumSteps[TConfiguration]):
    """
    BDD-style step definitions for TerminalX UI operations using Selenium.

    Type Parameters:
        TConfiguration: The configuration type, must be a TerminalXConfiguration.
    """
    @Context.traced
    def amazon(self, driver: WebDriver) -> Self:
        """
        Sets the Selenium WebDriver and navigates to the landing page.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
        Returns:
            Self: The current step instance for chaining.
        """
        self._web_driver = driver
        self._web_driver.get(self.configured.landing_page)
        return self

    @Context.traced
    def searching_for(self, text: str) -> Self:
        return (self.typing(By.id("twotabsearchtextbox"), text)
                .and_.clicking(By.id("nav-search-submit-button")))

    @Context.traced
    def selecting_result(self, index: int) -> Self:
        return self.clicking(
            By.xpath(f"//div[@role='listitem']//img[@data-image-index={index}]"))

    @Context.traced
    def adding_to_cart(self) -> Self:
        return self.clicking(By.id("add-to-cart-button"))

    @Context.traced
    def proceed_to_checkout(self) -> Self:
        return self.clicking(
            By.xpath("//input[@name='proceedToRetailCheckout']"))

    @Context.traced
    def signin_required(self) -> Self:
        return self.the_element(
            By.id("?"),
            adapted_object(
                lambda element: element.text,
                is_("Sign in or create account")))
