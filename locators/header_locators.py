from selenium.webdriver.common.by import By


class HeaderLocators:
    CART_LINK = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
    MENU_BTN = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
