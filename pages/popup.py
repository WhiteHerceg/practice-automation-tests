import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class Popup(BasePage):
    def __init__(self, driver, xpath, title):
        super().__init__(driver)
        self.xpath = xpath
        self.title = title
        self.container = (By.XPATH, xpath)
        self.close_button = (By.XPATH, f"{xpath}//button[contains(@class, 'pum-close')]")

    def is_open(self, timeout=10):
        return self.is_displayed(self.container, timeout)

    def is_closed(self, timeout=5):
        return self.is_hidden(self.container, timeout)

    def is_close_button_displayed(self):
        return self.is_displayed(self.close_button, 5)

    @property
    def text(self):
        return self.visible(self.container).text

    def close(self):
        with allure.step(f"Закрыть окно «{self.title}»"):
            self.click(self.close_button)
            self.wait.until(lambda _: not self._any_displayed(self.container))
