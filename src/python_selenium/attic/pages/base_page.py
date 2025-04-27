# pages/base_page.py
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)  # default 10s wait

    def open_url(self, url):
        self.driver.get(url)

    def wait_for_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))
