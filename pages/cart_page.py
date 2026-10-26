from framework.core.base_page import BasePage
from locators.cart_locators import CartLocators
from pages.checkout_page import CheckoutInfoPage


class CartPage(BasePage):
    PATH = "cart.html"

    def item_names(self) -> list[str]:
        self.wait_for_url_contains(self.PATH)
        return self.get_texts(CartLocators.ITEM_NAMES)

    def checkout(self) -> CheckoutInfoPage:
        self.click(CartLocators.CHECKOUT_BTN)
        return self.go_to(CheckoutInfoPage)
