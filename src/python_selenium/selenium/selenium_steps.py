from dataclasses import dataclass
from typing import Callable, List, Optional, Protocol, Self, Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from python_selenium.testing.abstract_configuration import AbstractConfiguration
from python_selenium.testing.generic_steps import GenericSteps

class SearchContext(Protocol):
    def find_element(self, by: str, value: Optional[str]) -> WebElement:
        ...

    def find_elements(self, by: str, value: Optional[str]) -> List[WebElement]:
        ...

@dataclass(frozen=True)
class Locator:
    by: str
    value: str

    def as_tuple(self) -> Tuple[str, str]:
        return (self.by, self.value)


class SeleniumSteps[TConfiguration:AbstractConfiguration](GenericSteps[TConfiguration]):
    web_driver: WebDriver

    def clicking_once(self, element_supplier: Callable[[], WebElement]) -> Self:
        element_supplier().click()
        return self

    def clicking(self, element_supplier: Callable[[], WebElement]) -> Self:
        return self.retrying(lambda: self.clicking_once(element_supplier))

    def typing_once(self, element_supplier: Callable[[], WebElement], text: str) -> Self:
        element = element_supplier()
        element.clear()
        element.send_keys(text)
        return self

    def typing(self, element_supplier: Callable[[], WebElement], text: str) -> Self:
        return self.retrying(lambda: self.typing_once(element_supplier, text))

    def elements(self, locator: Locator, context: Optional[SearchContext] = None) -> List[WebElement]:
        return (context or self.web_driver).find_elements(*locator.as_tuple())

    def element(self, locator: Locator, context: Optional[SearchContext] = None) -> WebElement:
        return self._scroll_into_view((context or self.web_driver).find_element(*locator.as_tuple()))

    def _scroll_into_view(self, element: WebElement) -> WebElement:
        self.web_driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element) # type: ignore
        return element
