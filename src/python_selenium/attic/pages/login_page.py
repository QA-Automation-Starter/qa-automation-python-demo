# pages/login_page.py
import time
from selenium.webdriver.common.by import By
from python_selenium.attic.pages.base_page import BasePage

class LoginPage(BasePage):
    USERNAME_FIELD = (By.CSS_SELECTOR, "input#email")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "input#password")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    def login(self, username, password):
        self.wait_for_element(self.USERNAME_FIELD).send_keys(username)
        self.wait_for_element(self.PASSWORD_FIELD).send_keys(password)
        self.wait_for_element(self.SUBMIT_BUTTON).click()
        time.sleep(5)  # wait for login
