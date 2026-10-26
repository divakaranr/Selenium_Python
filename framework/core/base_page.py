"""BasePage: the parent of every page object and component.

Every interaction waits explicitly for the right element state; there are no sleeps
or implicit waits. Locators are (By, value) tuples from the locators/ package.
"""
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from framework.utils.logger import get_logger

Locator = tuple[str, str]


class BasePage:
    # URL path relative to base_url, used by open(). Override in each page.
    PATH = ""

    def __init__(self, driver: WebDriver, base_url: str = "", timeout: int = 10):
        self.driver = driver
        self.base_url = base_url
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
        self.log = get_logger(type(self).__name__)

    def go_to(self, page_cls):
        """Build another page object that shares this page's driver and settings."""
        return page_cls(self.driver, self.base_url, self.timeout)

    # ---------- navigation ----------
    def open(self, path: str | None = None):
        url = f"{self.base_url}/{(self.PATH if path is None else path).lstrip('/')}"
        self.log.info("Open %s", url)
        self.driver.get(url)
        return self

    @property
    def title(self) -> str:
        return self.driver.title

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    def wait_for_url_contains(self, fragment: str) -> None:
        self.wait.until(EC.url_contains(fragment), f"URL never contained '{fragment}'")

    # ---------- finding ----------
    def find(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.presence_of_element_located(locator), f"Not present: {locator}")

    def find_visible(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator), f"Not visible: {locator}")

    def find_all(self, locator: Locator) -> list[WebElement]:
        """Wait for at least one match and return all of them, or [] after the timeout."""
        try:
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            return []

    def is_present(self, locator: Locator) -> bool:
        """Check right now, without waiting."""
        return len(self.driver.find_elements(*locator)) > 0

    def is_visible(self, locator: Locator, timeout: int | None = None) -> bool:
        """Wait up to `timeout` seconds (default: the page timeout) for visibility."""
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        try:
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    # ---------- actions ----------
    @staticmethod
    def _retry_on_stale(action):
        # Re-renders (React, etc.) can detach an element between locating and using it;
        # one retry re-locates it.
        try:
            return action()
        except StaleElementReferenceException:
            return action()

    def click(self, locator: Locator) -> None:
        self.log.info("Click %s", locator)
        self._retry_on_stale(
            lambda: self.wait.until(EC.element_to_be_clickable(locator), f"Not clickable: {locator}").click()
        )

    def type(self, locator: Locator, text: str, clear: bool = True) -> None:
        self.log.info("Type into %s", locator)

        def _type():
            element = self.find_visible(locator)
            if clear:
                element.clear()
            element.send_keys(text)

        self._retry_on_stale(_type)

    def get_text(self, locator: Locator) -> str:
        return self._retry_on_stale(lambda: self.find_visible(locator).text.strip())

    def get_texts(self, locator: Locator) -> list[str]:
        return self._retry_on_stale(lambda: [e.text.strip() for e in self.find_all(locator)])

    def select_by_text(self, locator: Locator, text: str) -> None:
        self.log.info("Select '%s' in %s", text, locator)
        self._retry_on_stale(lambda: Select(self.find_visible(locator)).select_by_visible_text(text))

    def scroll_into_view(self, locator: Locator) -> WebElement:
        element = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        return element
