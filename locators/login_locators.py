from selenium.webdriver.common.by import By


class LoginLocators:
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")
    ERROR_MSG = (By.CSS_SELECTOR, "[data-test='error']")
