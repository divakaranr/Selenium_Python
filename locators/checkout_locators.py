from selenium.webdriver.common.by import By


class CheckoutInfoLocators:
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BTN = (By.ID, "continue")
    ERROR_MSG = (By.CSS_SELECTOR, "[data-test='error']")


class CheckoutOverviewLocators:
    ITEM_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    SUBTOTAL = (By.CSS_SELECTOR, "[data-test='subtotal-label']")
    TOTAL = (By.CSS_SELECTOR, "[data-test='total-label']")
    FINISH_BTN = (By.ID, "finish")


class CheckoutCompleteLocators:
    COMPLETE_HEADER = (By.CSS_SELECTOR, "[data-test='complete-header']")
    BACK_HOME_BTN = (By.ID, "back-to-products")
