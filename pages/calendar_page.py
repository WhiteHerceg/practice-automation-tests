from datetime import date, datetime

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class CalendarPage(BasePage):
    path = "/calendars/"

    DATE_INPUT = (By.CSS_SELECTOR, "input[placeholder='YYYY-MM-DD']")
    SUBMIT = (
        By.XPATH,
        "//input[@placeholder='YYYY-MM-DD']/ancestor::form"
        "//*[self::button or self::input][@type='submit']",
    )
    CONFIRMATION = (By.XPATH, "//*[contains(text(), 'Thank you for your response')]")

    CALENDAR = (By.ID, "ui-datepicker-div")
    TITLE = (By.CSS_SELECTOR, "#ui-datepicker-div .ui-datepicker-title")
    NEXT_MONTH = (By.CSS_SELECTOR, "#ui-datepicker-div .ui-datepicker-next")
    PREV_MONTH = (By.CSS_SELECTOR, "#ui-datepicker-div .ui-datepicker-prev")
    MONTH_SELECT = (By.CSS_SELECTOR, "#ui-datepicker-div select.ui-datepicker-month")
    YEAR_SELECT = (By.CSS_SELECTOR, "#ui-datepicker-div select.ui-datepicker-year")
    TODAY_CELL = (By.CSS_SELECTOR, "#ui-datepicker-div td.ui-datepicker-today")

    @property
    def date_value(self):
        return self.value_of(self.DATE_INPUT)

    @property
    def placeholder(self):
        return self.find(self.DATE_INPUT).get_attribute("placeholder")

    def is_calendar_displayed(self, timeout=0):
        return self.is_displayed(self.CALENDAR, timeout)

    def is_calendar_hidden(self, timeout=3):
        return self.is_hidden(self.CALENDAR, timeout)

    def is_today_highlighted(self):
        return self.is_displayed(self.TODAY_CELL, 3)

    @allure.step("Открыть календарь кликом по полю даты")
    def open_calendar(self):
        self.click(self.DATE_INPUT)
        self.visible(self.CALENDAR)

    @allure.step("Кликнуть вне календаря")
    def click_outside(self):
        self.click(self.HEADING)

    def displayed_month(self):
        month_selects = self.driver.find_elements(*self.MONTH_SELECT)
        year_selects = self.driver.find_elements(*self.YEAR_SELECT)
        if month_selects and year_selects:
            month = int(Select(month_selects[0]).first_selected_option.get_attribute("value")) + 1
            year = int(Select(year_selects[0]).first_selected_option.get_attribute("value"))
            return year, month
        title = " ".join(self.visible(self.TITLE).text.split())
        parsed = datetime.strptime(title, "%B %Y")
        return parsed.year, parsed.month

    def _shift(self, locator, steps):
        for _ in range(steps):
            before = self.displayed_month()
            self.click(locator)
            self.wait.until(lambda _: self.displayed_month() != before)

    @allure.step("Перейти на следующий месяц")
    def next_month(self):
        self._shift(self.NEXT_MONTH, 1)

    @allure.step("Перейти на предыдущий месяц")
    def previous_month(self):
        self._shift(self.PREV_MONTH, 1)

    def go_to_month(self, target: date):
        year, month = self.displayed_month()
        diff = (target.year - year) * 12 + (target.month - month)
        if diff > 0:
            self._shift(self.NEXT_MONTH, diff)
        elif diff < 0:
            self._shift(self.PREV_MONTH, -diff)

    @allure.step("Выбрать дату {target} в календаре")
    def select_date(self, target: date):
        self.open_calendar()
        self.go_to_month(target)
        day = (
            By.XPATH,
            "//div[@id='ui-datepicker-div']//td[@data-handler='selectDay']"
            f"/a[normalize-space()='{target.day}']",
        )
        self.click(day)
        self.wait.until(lambda _: self.date_value == target.isoformat())

    @allure.step("Ввести дату вручную: {text}")
    def enter_date(self, text):
        self.type_text(self.DATE_INPUT, text)

    @allure.step("Нажать Submit")
    def submit(self):
        self.click(self.SUBMIT)

    def is_confirmation_displayed(self, timeout=10):
        return self.is_displayed(self.CONFIRMATION, timeout)
