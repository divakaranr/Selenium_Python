# Selenium Python UI Framework

A base framework for UI-testing a web application with **Selenium 4 + pytest**. It uses the Page Object Model, keeps locators in their own package, uses only explicit waits, and is driven by config. It produces HTML reports with failure screenshots and runs in GitHub Actions.

The sample tests target the demo shop [saucedemo.com](https://www.saucedemo.com).

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

You don't need to download any drivers. Selenium Manager fetches the right driver, and a browser too if none is installed.

## Running tests

| Goal | Command |
|---|---|
| Everything (default browser from config) | `pytest` |
| Smoke tests only | `pytest -m smoke` |
| Another browser | `pytest --browser firefox` (`chrome`, `firefox`, `edge`) |
| Headless | `pytest --headless` |
| Another environment | `pytest --env staging` |
| Override the URL | `pytest --base-url https://my-app.test` |
| Parallel | `pytest -n auto` |
| Retry flaky tests | `pytest --reruns 2` |

The report is written to `reports/report.html`. Failure screenshots are embedded in the report and also saved to `screenshots/`. Logs go to `logs/run.log`.

**Settings precedence:** CLI option, then environment variable (`ENV`, `BROWSER`, `HEADLESS`, `BASE_URL`), then `config/config.yaml`. Put secrets in a git-ignored `.env` file, never in YAML.

## Structure

```
config/        config.yaml (per-environment values) + settings.py (loader)
framework/
  core/        driver_factory.py (creates browsers), base_page.py (wait-wrapped actions)
  components/  UI pieces shared by many pages (Header)
  utils/       logger, waits, screenshot, data_loader
locators/      one class per page: (By, value) tuples only
pages/         page objects: behaviour only, using locators/
tests/         conftest.py (options, fixtures, failure hook) + test files
test_data/     JSON/YAML/CSV data for data-driven tests
```

## Adding a new page

1. **Locators:** create `locators/profile_locators.py`:
   ```python
   from selenium.webdriver.common.by import By

   class ProfileLocators:
       NAME_INPUT = (By.ID, "name")
       SAVE_BTN = (By.CSS_SELECTOR, "[data-test='save']")
   ```
   Prefer selectors in this order: `id`, then `data-test`, then CSS, with XPath as a last resort. For dynamic elements, add a `@staticmethod` that returns a tuple (see `InventoryLocators.add_to_cart_btn`).

2. **Page object:** create `pages/profile_page.py`:
   ```python
   from framework.core.base_page import BasePage
   from locators.profile_locators import ProfileLocators

   class ProfilePage(BasePage):
       PATH = "profile"

       def update_name(self, name: str) -> "ProfilePage":
           self.type(ProfileLocators.NAME_INPUT, name)
           self.click(ProfileLocators.SAVE_BTN)
           return self
   ```
   Methods that navigate return the next page through `self.go_to(NextPage)`, so tests can chain calls.

3. **Test:** use fixtures from `conftest.py` (`driver`, `settings`, `login_page`, `logged_in`, `users`) and add a marker:
   ```python
   @pytest.mark.regression
   def test_update_name(driver, settings):
       page = ProfilePage(driver, settings.base_url, settings.explicit_wait).open()
       page.update_name("New Name")
   ```

## Conventions

- Tests never call Selenium directly or use raw locators. Go through page objects.
- Don't use `time.sleep`. `BasePage` waits for each element to be present, visible, or clickable, and retries once on stale elements.
- Each test gets its own browser (function-scoped `driver`), so tests are independent and safe to run in parallel.
- To use a new application, change `base_url` in `config/config.yaml` and replace the saucedemo locators, pages, and tests. The `framework/` and `config/` packages stay the same.

## CI

`.github/workflows/ui-tests.yml` runs on every push and PR, headless and in parallel, across a Chrome and Firefox matrix. It uploads the report, screenshots, and logs as build artifacts. When triggered by hand, it accepts an optional marker (for example `smoke`).
