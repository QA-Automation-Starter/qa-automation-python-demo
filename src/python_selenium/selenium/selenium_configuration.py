from functools import cached_property
from typing import final
from python_selenium.testing.abstract_configuration import AbstractConfiguration
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class SeleniumConfiguration(AbstractConfiguration):

    @cached_property
    @final
    def ui_url(self) -> str:
        return self.parser["ui"]["url"]

    @property
    @final
    def web_driver(self) -> WebDriver:
        options = Options()
        options.add_argument("--start-maximized")  # type: ignore

        return Chrome(
            options,
            Service(ChromeDriverManager().install()))
