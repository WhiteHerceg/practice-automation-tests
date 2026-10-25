import allure
import pytest

VALID_NAME = "Иван Петров"
VALID_EMAIL = "ivan.petrov@example.com"
VALID_MESSAGE = "Тестовое сообщение из автотеста"


@allure.epic("Practice Automation")
@allure.feature("Модальные окна")
@pytest.mark.positive
class TestModalsPositive:

    @allure.title("Заголовок страницы — Modals")
    @allure.severity(allure.severity_level.MINOR)
    def test_page_heading(self, modals_page):
        assert modals_page.heading == "Modals"

    @allure.title("На странице есть кнопки Simple Modal и Form Modal")
    @allure.severity(allure.severity_level.NORMAL)
    def test_buttons_displayed(self, modals_page):
        assert modals_page.are_buttons_displayed()

    @allure.title("Кнопка Simple Modal открывает простое модальное окно")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_open_simple_modal(self, modals_page):
        modal = modals_page.open_simple_modal()
        assert modal.is_open(3)

    @allure.title("Простое модальное окно содержит ожидаемый текст")
    @allure.severity(allure.severity_level.NORMAL)
    def test_simple_modal_text(self, modals_page):
        modal = modals_page.open_simple_modal()
        assert "simple modal" in modal.text

    @allure.title("Простое модальное окно закрывается по кнопке ×")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_close_simple_modal(self, modals_page):
        modal = modals_page.open_simple_modal()
        modal.close()
        assert modal.is_closed()

    @allure.title("Кнопка Form Modal открывает окно с формой")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_open_form_modal(self, modals_page):
        modal = modals_page.open_form_modal()
        assert modal.is_open(3)

    @allure.title("В окне с формой есть поля Name, Email, Message и кнопка Submit")
    @allure.severity(allure.severity_level.NORMAL)
    def test_form_modal_fields(self, modals_page):
        modal = modals_page.open_form_modal()
        assert modal.fields_displayed()

    @allure.title("Окно с формой закрывается по кнопке ×")
    @allure.severity(allure.severity_level.NORMAL)
    def test_close_form_modal(self, modals_page):
        modal = modals_page.open_form_modal()
        modal.close()
        assert modal.is_closed()

    @allure.title("Отправка полностью заполненной формы показывает подтверждение")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_submit_filled_form(self, modals_page):
        modal = modals_page.open_form_modal()
        modal.fill(VALID_NAME, VALID_EMAIL, VALID_MESSAGE)
        modal.submit()
        assert modal.is_confirmation_displayed()

    @allure.title("Отправка формы только с обязательным полем Name проходит успешно")
    @allure.severity(allure.severity_level.NORMAL)
    def test_submit_form_with_name_only(self, modals_page):
        modal = modals_page.open_form_modal()
        modal.fill(name=VALID_NAME)
        modal.submit()
        assert modal.is_confirmation_displayed()


@allure.epic("Practice Automation")
@allure.feature("Модальные окна")
@pytest.mark.negative
class TestModalsNegative:

    @allure.title("Модальные окна скрыты при загрузке страницы")
    @allure.severity(allure.severity_level.NORMAL)
    def test_modals_hidden_by_default(self, modals_page):
        assert modals_page.simple_modal.is_closed(2)
        assert modals_page.form_modal.is_closed(2)

    @allure.title("Простое окно не отображается после закрытия")
    @allure.severity(allure.severity_level.NORMAL)
    def test_simple_modal_stays_closed(self, modals_page):
        modal = modals_page.open_simple_modal()
        modal.close()
        assert modal.is_closed(3)
        assert modals_page.form_modal.is_closed(1)

    @allure.title("Форма с пустым обязательным полем Name не отправляется")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_submit_empty_form(self, modals_page):
        modal = modals_page.open_form_modal()
        modal.submit()
        assert not modal.is_confirmation_displayed(timeout=2)
        assert modal.is_open(1)

    @allure.title("Форма без имени, но с email и сообщением не отправляется")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_submit_without_name(self, modals_page):
        modal = modals_page.open_form_modal()
        modal.fill(email=VALID_EMAIL, message=VALID_MESSAGE)
        modal.submit()
        assert not modal.is_confirmation_displayed(timeout=2)

    @allure.title("Некорректный email помечается как невалидный и форма не отправляется")
    @allure.severity(allure.severity_level.NORMAL)
    def test_invalid_email(self, modals_page):
        modal = modals_page.open_form_modal()
        modal.fill(name=VALID_NAME, email="не-email")
        assert not modals_page.is_field_valid(modal.email_input)
        modal.submit()
        assert not modal.is_confirmation_displayed(timeout=2)
