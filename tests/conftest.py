import pytest
from pytest_metadata.plugin import metadata_key

from config.settings import load_settings
from framework.core.driver_factory import create_driver
from framework.utils.data_loader import load_data
from framework.utils.logger import get_logger
from framework.utils.screenshot import capture_screenshot
from pages.login_page import LoginPage

log = get_logger("conftest")


def pytest_addoption(parser):
    group = parser.getgroup("ui", "UI test options")
    group.addoption("--browser", default=None, help="chrome | firefox | edge")
    group.addoption("--env", default=None, help="Environment block from config/config.yaml")
    group.addoption("--headless", action="store_true", default=None, help="Run browsers headless")
    group.addoption("--base-url", default=None, help="Override the environment's base_url")


def pytest_configure(config):
    config.ui_settings = load_settings(
        env=config.getoption("--env"),
        browser=config.getoption("--browser"),
        headless=config.getoption("--headless"),
        base_url=config.getoption("--base-url"),
    )
    s = config.ui_settings
    config.stash[metadata_key].update(
        {"Environment": s.env, "Base URL": s.base_url, "Browser": s.browser, "Headless": str(s.headless)}
    )


def pytest_html_report_title(report):
    report.title = "UI Test Report"


# ---------- fixtures ----------
@pytest.fixture(scope="session")
def settings(pytestconfig):
    return pytestconfig.ui_settings


@pytest.fixture
def driver(settings):
    driver = create_driver(settings)
    yield driver
    driver.quit()


@pytest.fixture
def users():
    return load_data("users.json")


@pytest.fixture
def login_page(driver, settings) -> LoginPage:
    return LoginPage(driver, settings.base_url, settings.explicit_wait).open()


@pytest.fixture
def logged_in(login_page, users):
    """Inventory page after logging in as the standard user."""
    user = users["standard"]
    return login_page.login(user["username"], user["password"])


# ---------- failure screenshots ----------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when not in ("setup", "call") or not report.failed:
        return

    driver = item.funcargs.get("driver")
    if driver is None:
        return

    try:
        capture_screenshot(driver, item.name)
        html = item.config.pluginmanager.getplugin("html")
        if html:
            extras = getattr(report, "extras", [])
            extras.append(html.extras.url(driver.current_url))
            extras.append(html.extras.png(driver.get_screenshot_as_base64()))
            report.extras = extras
    except Exception:  # never let reporting hide the real failure
        log.warning("Could not capture failure screenshot for %s", item.nodeid, exc_info=True)
