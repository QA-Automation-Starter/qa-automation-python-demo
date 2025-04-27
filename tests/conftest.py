import pytest
import json
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session")
def random_user():
    """
    Reads users from users.json and returns a random user from the list.
    """
    with open("tests/resources/users.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    users = data["users"]
    return random.choice(users)

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()