# tests/test_terminalx.py

import pytest
import time

from python_selenium.attic.pages.landing_page import LandingPage
from python_selenium.attic.pages.login_page import LoginPage
from python_selenium.attic.pages.search_results_page import SearchResultsPage
from python_selenium.attic.pages.product_page import ProductPage

@pytest.mark.usefixtures("driver", "random_user")
def test_terminalx_flow(driver, random_user):
    # 1) Landing Page
    landing = LandingPage(driver)
    landing.open()

    # 2) Login
    landing.click_login()
    login_page = LoginPage(driver)
    login_page.login(random_user["username"], random_user["password"])

    # 3) Enter “hello” & 4) Check dropdown for "hello kitty"
    landing.enter_search_text("hello")
    dropdown_texts = landing.get_dropdown_results()
    for text in dropdown_texts:
        if "hello kitty" not in text.lower():
            raise AssertionError(f"Dropdown result '{text}' missing 'hello kitty'")

    # Submit the search => to results page
    landing.submit_search()
    results_page = SearchResultsPage(driver)

    # 5) Check products sorted ascending by price
    prices = results_page.get_all_prices()
    if prices != sorted(prices):
        raise AssertionError(f"Prices not in ascending order: {prices}")

    # 6) Go to 3rd result
    results_page.click_nth_product(n=3)
    product_page = ProductPage(driver)

    # 7) Check price is present & font-size ~ 1.8rem => ~28.8px if base=16px
    product_price = product_page.get_price_text()
    if not product_price:
        raise AssertionError("No price text found on product page.")

    font_size = product_page.get_price_font_size()
    # Usually returns something like "28.8px" for 1.8rem, or "1.8rem"
    if "px" in font_size.lower():
        px_value = float(font_size.replace("px", ""))
        if abs(px_value - 28.8) > 1.0:
            raise AssertionError(f"Expected ~28.8px for 1.8rem, got {px_value}px")
    else:
        # Possibly "1.8rem"
        if not font_size.startswith("1.8"):
            raise AssertionError(f"Expected 1.8rem, got {font_size}")

    print("All steps completed successfully!")
