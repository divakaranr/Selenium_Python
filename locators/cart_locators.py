from selenium.webdriver.common.by import By


class CartLocators:
    ITEM_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    CHECKOUT_BTN = (By.ID, "checkout")
    CONTINUE_SHOPPING_BTN = (By.ID, "continue-shopping")
