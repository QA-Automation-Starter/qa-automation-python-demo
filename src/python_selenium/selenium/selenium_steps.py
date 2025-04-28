from dataclasses import dataclass
from typing import Callable, List, Optional, Protocol, Self, Tuple, Union, overload
from selenium.webdriver.common.by import By as _By
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

class By:

    @staticmethod
    def id(value: str) -> Locator:
        return Locator(_By.ID, value)

    @staticmethod
    def xpath(value: str) -> Locator:
        return Locator(_By.XPATH, value)

    @staticmethod
    def link_text(value: str) -> Locator:
        return Locator(_By.LINK_TEXT, value)

    @staticmethod
    def partial_link_text(value: str) -> Locator:
        return Locator(_By.PARTIAL_LINK_TEXT, value)

    @staticmethod
    def name(value: str) -> Locator:
        return Locator(_By.NAME, value)

    @staticmethod
    def tag_name(value: str) -> Locator:
        return Locator(_By.TAG_NAME, value)

    @staticmethod
    def class_name(value: str) -> Locator:
        return Locator(_By.CLASS_NAME, value)

    @staticmethod
    def css_selector(value: str) -> Locator:
        return Locator(_By.CSS_SELECTOR, value)

ElementSupplier = Callable[[], WebElement]
LocatorOrSupplier = Union[Locator, ElementSupplier]

class SeleniumSteps[TConfiguration:AbstractConfiguration](GenericSteps[TConfiguration]):
    web_driver: WebDriver

    def clicking_once(self, element_supplier: ElementSupplier) -> Self:
        element_supplier().click()
        return self

    @overload
    def clicking(self, element: Locator) -> Self: ...

    @overload
    def clicking(self, element: ElementSupplier) -> Self: ...

    def clicking(self, element: LocatorOrSupplier) -> Self:
        return self.retrying(lambda: self.clicking_once(self._resolve(element)))

    def typing_once(self, element_supplier: ElementSupplier, text: str) -> Self:
        element = element_supplier()
        element.clear()
        element.send_keys(text)
        return self

    @overload
    def typing(self, element: Locator, text: str) -> Self: ...

    @overload
    def typing(self, element: ElementSupplier, text: str) -> Self: ...

    def typing(self, element: LocatorOrSupplier, text: str) -> Self:
        return self.retrying(lambda: self.typing_once(self._resolve(element), text))

    def elements(self, locator: Locator, context: Optional[SearchContext] = None) -> List[WebElement]:
        return (context or self.web_driver).find_elements(*locator.as_tuple())

    def element(self, locator: Locator, context: Optional[SearchContext] = None) -> WebElement:
        return self._scroll_into_view((context or self.web_driver).find_element(*locator.as_tuple()))

    def _scroll_into_view(self, element: WebElement) -> WebElement:
        self.web_driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element) # type: ignore
        return element

    def _resolve(self, element: LocatorOrSupplier) -> ElementSupplier:
        if isinstance(element, Locator):
            return lambda: self.element(element)
        return element