from functools import cached_property
from typing import final
from python_selenium.testing.abstract_configuration import AbstractConfiguration
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class SeleniumConfiguration(AbstractConfiguration):

    @cached_property
    @final
    def ui_url(self) -> str:
        return self.parser["ui"]["url"]

    @cached_property
    @final
    def web_driver_service(self) -> Service:
        # NOTE may add support for providing different services per configuration
        return Service(ChromeDriverManager().install())
