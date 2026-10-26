"""Custom expected conditions and wait helpers for cases Selenium's built-ins don't cover."""
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait


class element_text_is_not_empty:
    """Wait until the element located by `locator` shows non-blank text. Returns the text."""

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            text = driver.find_element(*self.locator).text.strip()
        except StaleElementReferenceException:
            return False
        return text or False


class number_of_elements_to_be:
    """Wait until exactly `count` elements match `locator`. Returns the elements."""

    def __init__(self, locator, count: int):
        self.locator = locator
        self.count = count

    def __call__(self, driver):
        elements = driver.find_elements(*self.locator)
        return elements if len(elements) == self.count else False


def wait_until(driver, condition, timeout: int, message: str = ""):
    """Run any condition (a callable taking the driver) with an explicit timeout."""
    return WebDriverWait(driver, timeout).until(condition, message)
