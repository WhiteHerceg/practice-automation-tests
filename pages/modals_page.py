import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.popup import Popup

CONTAINER = "//div[contains(@class, 'pum-container')]"


class SimpleModal(Popup):
    def __init__(self, driver):
        super().__init__(driver, f"{CONTAINER}[contains(., 'a simple modal')]", "Simple Modal")


class FormModal(Popup):
    def __init__(self, driver):
        super().__init__(
            driver,
            f"{CONTAINER}[contains(., 'Please enter your contact info below')]",
            "Modal Containing A Form",
        )
        self.name_input = self._field("Name", "input")
        self.email_input = self._field("Email", "input")
        self.message_input = self._field("Message", "textarea")
        self.submit_button = (
            By.XPATH,
            f"{self.xpath}//*[self::button or self::input][@type='submit']",
        )
        self.confirmation = (
            By.XPATH,
            f"{self.xpath}//*[contains(text(), 'Thank you for your response')]",
        )

    def _field(self, label, tag):
        label_xpath = f"{self.xpath}//label[contains(normalize-space(), '{label}')]"
        return (By.XPATH, f"({label_xpath}//{tag} | {label_xpath}/following::{tag}[1])[1]")

    def fill(self, name="", email="", message=""):
        with allure.step("Заполнить форму в модальном окне"):
            if name:
                self.type_text(self.name_input, name)
            if email:
                self.type_text(self.email_input, email)
            if message:
                self.type_text(self.message_input, message)

    def submit(self):
        with allure.step("Нажать Submit в модальном окне"):
            self.click(self.submit_button)

    def fields_displayed(self):
        return all(
            self.is_displayed(locator, 3)
            for locator in (self.name_input, self.email_input, self.message_input, self.submit_button)
        )

    def is_confirmation_displayed(self, timeout=10):
        return self.is_displayed(self.confirmation, timeout)


class ModalsPage(BasePage):
    path = "/modals/"

    SIMPLE_BUTTON = (
        By.XPATH,
        "//*[@id='simpleModal'] | //*[self::button or self::a][normalize-space()='Simple Modal']",
    )
    FORM_BUTTON = (
        By.XPATH,
        "//*[@id='formModal'] | //*[self::button or self::a][normalize-space()='Form Modal']",
    )

    def __init__(self, driver):
        super().__init__(driver)
        self.simple_modal = SimpleModal(driver)
        self.form_modal = FormModal(driver)

    def are_buttons_displayed(self):
        return self.is_displayed(self.SIMPLE_BUTTON, 3) and self.is_displayed(self.FORM_BUTTON, 3)

    @allure.step("Нажать кнопку Simple Modal")
    def open_simple_modal(self):
        self.click(self.SIMPLE_BUTTON)
        self.simple_modal.visible(self.simple_modal.container)
        return self.simple_modal

    @allure.step("Нажать кнопку Form Modal")
    def open_form_modal(self):
        self.click(self.FORM_BUTTON)
        self.form_modal.visible(self.form_modal.container)
        return self.form_modal
