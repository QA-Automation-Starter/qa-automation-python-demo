# pages/landing_page.py
import time
from selenium.webdriver.common.by import By
from python_selenium.attic.pages.base_page import BasePage

class LandingPage(BasePage):
    URL = "https://www.terminalx.com/"

    LOGIN_BUTTON = (By.XPATH, "(//div[contains(text(), 'התחברות')])")
    SEARCH_BOX = (By.CSS_SELECTOR, "input#search-input")
    DROPDOWN_RESULTS = (By.CSS_SELECTOR, "ul.suggestions-list li")

    def open(self):
        self.open_url(self.URL)
        time.sleep(3)  # quick wait for demo (use wait in production)

    def click_login(self):
        self.wait_for_element(self.LOGIN_BUTTON).click()
        time.sleep(2)

    def enter_search_text(self, text):
        self.wait_for_element(self.SEARCH_BOX).send_keys(text)
        time.sleep(2)  # wait for the dropdown suggestions
        return self  # Return self for fluent chaining

    def get_dropdown_results(self):
        """
        Return list of suggestion texts from the search dropdown.
        """
        elements = self.driver.find_elements(*self.DROPDOWN_RESULTS)
        return [el.text.strip() for el in elements]

    def submit_search(self):
        """
        Press 'Enter' or submit the search box to navigate to results.
        """
        search_box = self.wait_for_element(self.SEARCH_BOX)
        search_box.submit()
        time.sleep(5)  # let the results page load
