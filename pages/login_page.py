from framework.core.base_page import BasePage
from locators.login_locators import LoginLocators
from pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    PATH = ""

    def attempt_login(self, username: str, password: str) -> "LoginPage":
        """Submit credentials and stay on this page (use for negative cases)."""
        self.type(LoginLocators.USERNAME, username)
        self.type(LoginLocators.PASSWORD, password)
        self.click(LoginLocators.LOGIN_BTN)
        return self

    def login(self, username: str, password: str) -> InventoryPage:
        self.attempt_login(username, password)
        inventory = self.go_to(InventoryPage)
        inventory.wait_until_loaded()
        return inventory

    def is_displayed(self) -> bool:
        return self.is_visible(LoginLocators.LOGIN_BTN)

    @property
    def error_message(self) -> str:
        return self.get_text(LoginLocators.ERROR_MSG)
