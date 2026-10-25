import allure
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "https://practice-automation.com"
DEFAULT_TIMEOUT = 10


class BasePage:
    path = ""
    HEADING = (By.XPATH, "//h1[normalize-space()]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(
            driver, DEFAULT_TIMEOUT, ignored_exceptions=(StaleElementReferenceException,)
        )

    def open(self):
        with allure.step(f"Открыть страницу {BASE_URL}{self.path}"):
            self.driver.get(BASE_URL + self.path)
            self.wait.until(EC.visibility_of_element_located(self.HEADING))
        return self

    @property
    def heading(self):
        return self.visible(self.HEADING).text.strip()

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def scroll_to(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.scroll_to(element)
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

    def js_click(self, locator):
        element = self.find(locator)
        self.scroll_to(element)
        self.driver.execute_script("arguments[0].click();", element)

    def type_text(self, locator, text):
        element = self.visible(locator)
        self.scroll_to(element)
        element.clear()
        element.send_keys(text)

    def value_of(self, locator):
        return self.find(locator).get_attribute("value")

    def _any_displayed(self, locator):
        for element in self.driver.find_elements(*locator):
            try:
                if element.is_displayed():
                    return True
            except StaleElementReferenceException:
                continue
        return False

    def is_displayed(self, locator, timeout=2):
        try:
            WebDriverWait(self.driver, timeout).until(lambda _: self._any_displayed(locator))
            return True
        except TimeoutException:
            return False

    def is_hidden(self, locator, timeout=2):
        try:
            WebDriverWait(self.driver, timeout).until(lambda _: not self._any_displayed(locator))
            return True
        except TimeoutException:
            return False

    def is_field_valid(self, locator):
        return self.driver.execute_script(
            "return arguments[0].checkValidity();", self.find(locator)
        )
