import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from pages.base_page import BasePage

DRINKS = {
    "Water": "drink1",
    "Milk": "drink2",
    "Coffee": "drink3",
    "Wine": "drink4",
    "Ctrl-Alt-Delight": "drink5",
}

COLORS = {
    "Red": "color1",
    "Blue": "color2",
    "Yellow": "color3",
    "Green": "color4",
    "#FFC0CB": "color5",
}


class FormFieldsPage(BasePage):
    path = "/form-fields/"

    NAME = (By.ID, "name-input")
    PASSWORD = (By.CSS_SELECTOR, "input[type='password']")
    EMAIL = (By.ID, "email")
    MESSAGE = (By.ID, "message")
    SUBMIT = (By.ID, "submit-btn")
    AUTOMATION_SELECT = (By.ID, "automation")
    TOOLS = (By.XPATH, "//*[normalize-space()='Automation tools']/following::ul[1]/li")

    @allure.step("Заполнить поле Name: {name}")
    def fill_name(self, name):
        self.type_text(self.NAME, name)

    @allure.step("Заполнить поле Password")
    def fill_password(self, password):
        self.type_text(self.PASSWORD, password)

    @allure.step("Заполнить поле Email: {email}")
    def fill_email(self, email):
        self.type_text(self.EMAIL, email)

    @allure.step("Выбрать напиток: {drink}")
    def choose_drink(self, drink):
        locator = (By.ID, DRINKS[drink])
        if not self.find(locator).is_selected():
            self.js_click(locator)

    @allure.step("Выбрать цвет: {color}")
    def choose_color(self, color):
        self.js_click((By.ID, COLORS[color]))

    @allure.step("Ответить на вопрос «Do you like automation?»: {answer}")
    def choose_automation_answer(self, answer):
        Select(self.visible(self.AUTOMATION_SELECT)).select_by_visible_text(answer)

    def is_drink_selected(self, drink):
        return self.find((By.ID, DRINKS[drink])).is_selected()

    def is_color_selected(self, color):
        return self.find((By.ID, COLORS[color])).is_selected()

    @property
    def automation_answer(self):
        return Select(self.find(self.AUTOMATION_SELECT)).first_selected_option.text

    @allure.step("Получить список элементов из раздела Automation tools")
    def get_tools(self):
        self.wait.until(lambda d: len(d.find_elements(*self.TOOLS)) > 0)
        return [item.text.strip() for item in self.driver.find_elements(*self.TOOLS)]

    @allure.step("Заполнить Message списком инструментов через запятую")
    def fill_message_with_tools(self):
        message = ", ".join(self.get_tools())
        self.type_text(self.MESSAGE, message)
        return message

    @allure.step("Заполнить поле Message: {text}")
    def fill_message(self, text):
        self.type_text(self.MESSAGE, text)

    @property
    def message_value(self):
        return self.value_of(self.MESSAGE)

    def is_email_valid(self):
        return self.is_field_valid(self.EMAIL)

    @allure.step("Нажать Submit")
    def submit(self):
        self.click(self.SUBMIT)

    def read_alert(self, timeout=5):
        try:
            alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        except TimeoutException:
            return None
        text = alert.text
        alert.accept()
        return text

    @allure.step("Нажать Submit и прочитать alert")
    def submit_and_read_alert(self, timeout=5):
        self.submit()
        return self.read_alert(timeout)
