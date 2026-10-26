from selenium.webdriver.common.by import By


def _slug(product_name: str) -> str:
    # "Sauce Labs Backpack" -> "sauce-labs-backpack", the form the app uses in data-test ids.
    return product_name.strip().lower().replace(" ", "-")


class InventoryLocators:
    TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    SORT_SELECT = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    ITEM_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    ITEM_PRICES = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")

    @staticmethod
    def add_to_cart_btn(product_name: str):
        return By.CSS_SELECTOR, f"[data-test='add-to-cart-{_slug(product_name)}']"

    @staticmethod
    def remove_btn(product_name: str):
        return By.CSS_SELECTOR, f"[data-test='remove-{_slug(product_name)}']"
