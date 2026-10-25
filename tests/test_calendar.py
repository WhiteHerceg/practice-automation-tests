from datetime import date, timedelta

import allure
import pytest

DATES_TO_SELECT = [
    date(2024, 3, 15),
    date(2024, 2, 29),
    date.today() + timedelta(days=90),
]


@allure.epic("Practice Automation")
@allure.feature("Календарь")
@pytest.mark.positive
class TestCalendarPositive:

    @allure.title("Заголовок страницы — Calendars")
    @allure.severity(allure.severity_level.MINOR)
    def test_page_heading(self, calendar_page):
        assert calendar_page.heading == "Calendars"

    @allure.title("В поле даты указан формат YYYY-MM-DD")
    @allure.severity(allure.severity_level.MINOR)
    def test_date_input_placeholder(self, calendar_page):
        assert calendar_page.placeholder == "YYYY-MM-DD"

    @allure.title("Клик по полю даты открывает календарь")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_calendar_opens_on_click(self, calendar_page):
        calendar_page.open_calendar()
        assert calendar_page.is_calendar_displayed(3)

    @allure.title("В открытом календаре подсвечен сегодняшний день")
    @allure.severity(allure.severity_level.NORMAL)
    def test_today_is_highlighted(self, calendar_page):
        calendar_page.open_calendar()
        assert calendar_page.is_today_highlighted()

    @allure.title("Выбор даты {target} через календарь")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("target", DATES_TO_SELECT, ids=str)
    def test_select_date_from_calendar(self, calendar_page, target):
        calendar_page.select_date(target)
        assert calendar_page.date_value == target.isoformat()

    @allure.title("Календарь закрывается после выбора даты")
    @allure.severity(allure.severity_level.NORMAL)
    def test_calendar_closes_after_selection(self, calendar_page):
        calendar_page.select_date(date(2024, 3, 15))
        assert calendar_page.is_calendar_hidden()

    @allure.title("Переключение месяцев вперёд и назад")
    @allure.severity(allure.severity_level.NORMAL)
    def test_month_navigation(self, calendar_page):
        calendar_page.open_calendar()
        year, month = calendar_page.displayed_month()
        expected_next = (year + month // 12, month % 12 + 1)
        calendar_page.next_month()
        assert calendar_page.displayed_month() == expected_next
        calendar_page.previous_month()
        assert calendar_page.displayed_month() == (year, month)

    @allure.title("Дата, введённая вручную, сохраняется в поле")
    @allure.severity(allure.severity_level.NORMAL)
    def test_manual_date_entry(self, calendar_page):
        calendar_page.enter_date("2025-12-31")
        assert calendar_page.date_value == "2025-12-31"

    @allure.title("Календарь показывает месяц введённой вручную даты")
    @allure.severity(allure.severity_level.NORMAL)
    def test_calendar_follows_manual_date(self, calendar_page):
        calendar_page.enter_date("2025-12-31")
        calendar_page.open_calendar()
        assert calendar_page.displayed_month() == (2025, 12)

    @allure.title("Отправка формы с выбранной датой показывает подтверждение")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_submit_selected_date(self, calendar_page):
        calendar_page.select_date(date(2024, 3, 15))
        calendar_page.submit()
        assert calendar_page.is_confirmation_displayed()


@allure.epic("Practice Automation")
@allure.feature("Календарь")
@pytest.mark.negative
class TestCalendarNegative:

    @allure.title("Календарь скрыт, пока пользователь не взаимодействует с полем")
    @allure.severity(allure.severity_level.NORMAL)
    def test_calendar_hidden_by_default(self, calendar_page):
        assert calendar_page.is_calendar_hidden()

    @allure.title("Поле даты пустое при загрузке страницы")
    @allure.severity(allure.severity_level.NORMAL)
    def test_date_input_empty_by_default(self, calendar_page):
        assert calendar_page.date_value == ""

    @allure.title("Календарь закрывается при клике вне поля без выбора даты")
    @allure.severity(allure.severity_level.NORMAL)
    def test_calendar_closes_on_outside_click(self, calendar_page):
        calendar_page.open_calendar()
        calendar_page.click_outside()
        assert calendar_page.is_calendar_hidden()
        assert calendar_page.date_value == ""

    @allure.title("Подтверждение не показывается до отправки формы")
    @allure.severity(allure.severity_level.NORMAL)
    def test_no_confirmation_before_submit(self, calendar_page):
        calendar_page.select_date(date(2024, 3, 15))
        assert not calendar_page.is_confirmation_displayed(timeout=2)
