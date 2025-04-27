# pages/product_page.py
from selenium.webdriver.common.by import By
from python_selenium.attic.pages.base_page import BasePage

class ProductPage(BasePage):
    PRICE_ELEMENT = (By.CSS_SELECTOR, "span.product-price")

    def get_price_text(self):
        return self.wait_for_element(self.PRICE_ELEMENT).text.strip()

    def get_price_font_size(self):
        """
        Return the computed 'font-size' (usually in px).
        """
        price_el = self.wait_for_element(self.PRICE_ELEMENT)
        return price_el.value_of_css_property("font-size")
