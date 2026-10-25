import os

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from pages.ads_page import AdsPage
from pages.calendar_page import CalendarPage
from pages.form_fields_page import FormFieldsPage
from pages.modals_page import ModalsPage


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", choices=("chrome", "firefox"))
    parser.addoption("--headless", action="store_true", default=False)


def _create_driver(name, headless):
    if name == "firefox":
        options = FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        if headless:
            options.add_argument("-headless")
        return webdriver.Firefox(options=options)

    options = ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-notifications")
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


@pytest.fixture
def driver(request):
    name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless") or os.getenv("CI") == "true"
    browser = _create_driver(name, headless)
    yield browser
    browser.quit()


@pytest.fixture
def calendar_page(driver):
    return CalendarPage(driver).open()


@pytest.fixture
def modals_page(driver):
    return ModalsPage(driver).open()


@pytest.fixture
def ads_page(driver):
    return AdsPage(driver).open()


@pytest.fixture
def form_page(driver):
    return FormFieldsPage(driver).open()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when in ("setup", "call") and report.failed:
        browser = item.funcargs.get("driver")
        if browser is not None:
            try:
                allure.attach(
                    browser.get_screenshot_as_png(),
                    name="Скриншот при ошибке",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception:
                pass
