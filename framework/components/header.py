from framework.core.base_page import BasePage
from locators.header_locators import HeaderLocators


class Header(BasePage):
    """Top bar shown on every page after login: cart link, badge and side menu."""

    @property
    def cart_count(self) -> int:
        if not self.is_present(HeaderLocators.CART_BADGE):
            return 0
        return int(self.get_text(HeaderLocators.CART_BADGE))

    def open_cart(self):
        from pages.cart_page import CartPage

        self.click(HeaderLocators.CART_LINK)
        return self.go_to(CartPage)

    def logout(self):
        # Imported here to avoid a cycle: LoginPage -> InventoryPage -> Header -> LoginPage.
        from pages.login_page import LoginPage

        self.click(HeaderLocators.MENU_BTN)
        self.click(HeaderLocators.LOGOUT_LINK)
        return self.go_to(LoginPage)
