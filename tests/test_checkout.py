import pytest

BACKPACK = "Sauce Labs Backpack"


@pytest.mark.smoke
def test_complete_purchase(logged_in, users):
    info = users["checkout"]

    cart = logged_in.add_to_cart(BACKPACK).header.open_cart()
    overview = cart.checkout().fill_info(info["first_name"], info["last_name"], info["postal_code"])
    assert overview.item_names() == [BACKPACK]
    assert overview.total > 0

    complete = overview.finish()
    assert complete.complete_header == "Thank you for your order!"


@pytest.mark.regression
def test_checkout_requires_first_name(logged_in):
    checkout_info = logged_in.add_to_cart(BACKPACK).header.open_cart().checkout()
    assert checkout_info.continue_with_missing_info() == "Error: First Name is required"
