import pytest

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@pytest.mark.regression
def test_sort_by_price_low_to_high(logged_in):
    prices = logged_in.sort_by("Price (low to high)").item_prices()
    assert prices == sorted(prices)


@pytest.mark.regression
def test_sort_by_name_z_to_a(logged_in):
    names = logged_in.sort_by("Name (Z to A)").item_names()
    assert names == sorted(names, reverse=True)


@pytest.mark.smoke
def test_add_and_remove_items_updates_cart_badge(logged_in):
    logged_in.add_to_cart(BACKPACK).add_to_cart(BIKE_LIGHT)
    assert logged_in.header.cart_count == 2

    logged_in.remove_from_cart(BACKPACK)
    assert logged_in.header.cart_count == 1


@pytest.mark.regression
def test_cart_lists_added_items(logged_in):
    logged_in.add_to_cart(BACKPACK).add_to_cart(BIKE_LIGHT)
    cart = logged_in.header.open_cart()
    assert cart.item_names() == [BACKPACK, BIKE_LIGHT]
