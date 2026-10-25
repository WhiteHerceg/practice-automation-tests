import allure
import pytest

EXPECTED_ALERT = "Message received!"


@allure.epic("Practice Automation")
@allure.feature("Форма")
@pytest.mark.positive
class TestFormFieldsPositive:

    @allure.title("Заголовок страницы — Form Fields")
    @allure.severity(allure.severity_level.MINOR)
    def test_page_heading(self, form_page):
        assert form_page.heading == "Form Fields"

    @allure.title("Раздел Automation tools содержит Selenium")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tools_list_contains_selenium(self, form_page):
        assert "Selenium" in form_page.get_tools()

    @allure.title("Поле Message заполняется списком Automation tools через запятую")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_message_filled_with_tools(self, form_page):
        tools = form_page.get_tools()
        message = form_page.fill_message_with_tools()
        assert message == ", ".join(tools)
        assert form_page.message_value == message
        assert form_page.message_value.count(", ") == len(tools) - 1

    @allure.title("Выбор напитка, цвета и ответа на вопрос об автоматизации")
    @allure.severity(allure.severity_level.NORMAL)
    def test_choose_options(self, form_page):
        form_page.choose_drink("Coffee")
        form_page.choose_color("Blue")
        form_page.choose_automation_answer("Yes")
        assert form_page.is_drink_selected("Coffee")
        assert form_page.is_color_selected("Blue")
        assert form_page.automation_answer == "Yes"

    @allure.title("Отправка заполненной формы со списком инструментов в Message")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_submit_form_with_tools_message(self, form_page):
        form_page.fill_name("Станислав")
        form_page.fill_password("Passw0rd!")
        form_page.choose_drink("Coffee")
        form_page.choose_color("Green")
        form_page.choose_automation_answer("Yes")
        form_page.fill_email("stas@example.com")
        form_page.fill_message_with_tools()
        assert form_page.submit_and_read_alert() == EXPECTED_ALERT


@allure.epic("Practice Automation")
@allure.feature("Форма")
@pytest.mark.negative
class TestFormFieldsNegative:

    @allure.title("Пустая форма не отправляется")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_submit_empty_form(self, form_page):
        assert form_page.submit_and_read_alert(timeout=2) != EXPECTED_ALERT

    @allure.title("Форма без имени, но с сообщением не отправляется")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_submit_without_name(self, form_page):
        form_page.fill_message_with_tools()
        assert form_page.submit_and_read_alert(timeout=2) != EXPECTED_ALERT

    @allure.title("Некорректный email помечается как невалидный")
    @allure.severity(allure.severity_level.NORMAL)
    def test_invalid_email(self, form_page):
        form_page.fill_email("не-email")
        assert not form_page.is_email_valid()
