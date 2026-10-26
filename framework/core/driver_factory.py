"""Create WebDriver instances.

Selenium Manager (bundled with Selenium 4.6+) resolves the matching driver binary, and
downloads a browser too if none is installed, so no driver setup is needed.
"""
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import Settings
from framework.utils.logger import get_logger

log = get_logger(__name__)

# Flags that keep Chromium stable in containers and CI runners.
_CHROMIUM_CI_ARGS = ("--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu")

# Turn off the password manager and the "password found in a data breach" popup,
# which otherwise appears after logging in with demo credentials.
_CHROMIUM_PREFS = {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
    "profile.password_manager_leak_detection": False,
}


def _chromium_options(options, settings: Settings):
    if settings.headless:
        options.add_argument("--headless=new")
    for arg in _CHROMIUM_CI_ARGS:
        options.add_argument(arg)
    options.add_argument("--disable-features=PasswordLeakDetection")
    options.add_experimental_option("prefs", _CHROMIUM_PREFS)
    return options


def _create_chrome(settings: Settings) -> WebDriver:
    return webdriver.Chrome(options=_chromium_options(webdriver.ChromeOptions(), settings))


def _create_edge(settings: Settings) -> WebDriver:
    return webdriver.Edge(options=_chromium_options(webdriver.EdgeOptions(), settings))


def _create_firefox(settings: Settings) -> WebDriver:
    options = webdriver.FirefoxOptions()
    if settings.headless:
        options.add_argument("-headless")
    return webdriver.Firefox(options=options)


# To add Selenium Grid later, register a "remote" builder here using webdriver.Remote.
_BUILDERS = {
    "chrome": _create_chrome,
    "edge": _create_edge,
    "firefox": _create_firefox,
}


def create_driver(settings: Settings) -> WebDriver:
    log.info("Starting %s (headless=%s)", settings.browser, settings.headless)
    driver = _BUILDERS[settings.browser](settings)
    driver.set_window_size(*settings.window_size)
    driver.set_page_load_timeout(settings.page_load_timeout)
    return driver
