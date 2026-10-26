"""The three checkout steps: your information -> overview -> complete."""
from framework.core.base_page import BasePage
from locators.checkout_locators import (
    CheckoutCompleteLocators,
    CheckoutInfoLocators,
    CheckoutOverviewLocators,
)


class CheckoutCompletePage(BasePage):
    PATH = "checkout-complete.html"

    @property
    def complete_header(self) -> str:
        return self.get_text(CheckoutCompleteLocators.COMPLETE_HEADER)


class CheckoutOverviewPage(BasePage):
    PATH = "checkout-step-two.html"

    def item_names(self) -> list[str]:
        return self.get_texts(CheckoutOverviewLocators.ITEM_NAMES)

    @property
    def total(self) -> float:
        # "Total: $32.39" -> 32.39
        return float(self.get_text(CheckoutOverviewLocators.TOTAL).split("$")[-1])

    def finish(self) -> CheckoutCompletePage:
        self.click(CheckoutOverviewLocators.FINISH_BTN)
        return self.go_to(CheckoutCompletePage)


class CheckoutInfoPage(BasePage):
    PATH = "checkout-step-one.html"

    def fill_info(self, first_name: str, last_name: str, postal_code: str) -> CheckoutOverviewPage:
        self.type(CheckoutInfoLocators.FIRST_NAME, first_name)
        self.type(CheckoutInfoLocators.LAST_NAME, last_name)
        self.type(CheckoutInfoLocators.POSTAL_CODE, postal_code)
        self.click(CheckoutInfoLocators.CONTINUE_BTN)
        return self.go_to(CheckoutOverviewPage)

    def continue_with_missing_info(self) -> str:
        """Click Continue without filling the form and return the validation error."""
        self.click(CheckoutInfoLocators.CONTINUE_BTN)
        return self.get_text(CheckoutInfoLocators.ERROR_MSG)
