import pytest

from framework.utils.data_loader import load_data

INVALID_LOGINS = load_data("users.json")["invalid_logins"]


@pytest.mark.smoke
def test_valid_login_opens_inventory(login_page, users):
    user = users["standard"]
    inventory = login_page.login(user["username"], user["password"])
    assert inventory.page_title == "Products"


@pytest.mark.smoke
@pytest.mark.parametrize("case", INVALID_LOGINS, ids=[c["id"] for c in INVALID_LOGINS])
def test_invalid_login_shows_error(login_page, case):
    login_page.attempt_login(case["username"], case["password"])
    assert login_page.error_message == case["error"]


@pytest.mark.regression
def test_logout_returns_to_login(logged_in):
    login_page = logged_in.header.logout()
    assert login_page.is_displayed()
