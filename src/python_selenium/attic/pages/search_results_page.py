# pages/search_results_page.py
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from python_selenium.attic.pages.base_page import BasePage

class SearchResultsPage(BasePage):
    PRODUCT_TILES = (By.CSS_SELECTOR, "div.product-tile")
    PRODUCT_PRICE = (By.CSS_SELECTOR, "span.product-price")

    def get_all_prices(self):
        """
        Return a list of numeric prices from all product tiles on the results page.
        """
        tiles = self.driver.find_elements(*self.PRODUCT_TILES)
        prices = []
        for tile in tiles:
            try:
                price_text = tile.find_element(*self.PRODUCT_PRICE).text
                # parse a float from e.g. "₪59.90"
                numeric_price = float("".join(ch for ch in price_text if ch.isdigit() or ch == "."))
                prices.append(numeric_price)
            except NoSuchElementException:
                pass
        return prices

    def click_nth_product(self, n=3):
        """
        Click the nth product (1-based). By default, clicks 3rd product.
        """
        tiles = self.driver.find_elements(*self.PRODUCT_TILES)
        if len(tiles) < n:
            raise ValueError(f"Not enough products to click item #{n}")
        tiles[n - 1].click()
        time.sleep(5)  # wait for product page to load
