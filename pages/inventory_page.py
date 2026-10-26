from framework.components.header import Header
from framework.core.base_page import BasePage
from locators.inventory_locators import InventoryLocators


class InventoryPage(BasePage):
    PATH = "inventory.html"

    @property
    def header(self) -> Header:
        return self.go_to(Header)

    def wait_until_loaded(self) -> "InventoryPage":
        self.wait_for_url_contains(self.PATH)
        self.find_visible(InventoryLocators.TITLE)
        return self

    @property
    def page_title(self) -> str:
        return self.get_text(InventoryLocators.TITLE)

    def sort_by(self, option_text: str) -> "InventoryPage":
        self.select_by_text(InventoryLocators.SORT_SELECT, option_text)
        return self

    def item_names(self) -> list[str]:
        return self.get_texts(InventoryLocators.ITEM_NAMES)

    def item_prices(self) -> list[float]:
        return [float(p.lstrip("$")) for p in self.get_texts(InventoryLocators.ITEM_PRICES)]

    def add_to_cart(self, product_name: str) -> "InventoryPage":
        self.click(InventoryLocators.add_to_cart_btn(product_name))
        self.find_visible(InventoryLocators.remove_btn(product_name))
        return self

    def remove_from_cart(self, product_name: str) -> "InventoryPage":
        self.click(InventoryLocators.remove_btn(product_name))
        self.find_visible(InventoryLocators.add_to_cart_btn(product_name))
        return self
