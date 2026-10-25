import allure
import pytest


@allure.epic("Practice Automation")
@allure.feature("Рекламные окна")
@pytest.mark.positive
class TestAdsPositive:

    @allure.title("Заголовок страницы — Ads")
    @allure.severity(allure.severity_level.MINOR)
    def test_page_heading(self, ads_page):
        assert ads_page.heading == "Ads"

    @allure.title("На странице есть ссылка Home в хлебных крошках")
    @allure.severity(allure.severity_level.MINOR)
    def test_home_link_displayed(self, ads_page):
        assert ads_page.is_home_link_displayed()

    @allure.title("Рекламное окно появляется через несколько секунд после загрузки")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_ad_appears(self, ads_page):
        assert ads_page.wait_for_ad()

    @allure.title("Рекламное окно содержит текст «I am an ad.»")
    @allure.severity(allure.severity_level.NORMAL)
    def test_ad_text(self, ads_page):
        ads_page.wait_for_ad()
        assert "I am an ad" in ads_page.ad.text

    @allure.title("Рекламное окно содержит заголовок «Hi»")
    @allure.severity(allure.severity_level.NORMAL)
    def test_ad_greeting(self, ads_page):
        ads_page.wait_for_ad()
        assert ads_page.ad.is_greeting_displayed()

    @allure.title("В рекламном окне отображается кнопка закрытия")
    @allure.severity(allure.severity_level.NORMAL)
    def test_ad_close_button_displayed(self, ads_page):
        ads_page.wait_for_ad()
        assert ads_page.ad.is_close_button_displayed()

    @allure.title("Рекламное окно закрывается по кнопке ×")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_close_ad(self, ads_page):
        ads_page.wait_for_ad()
        ads_page.ad.close()
        assert ads_page.ad.is_closed()

    @allure.title("После закрытия рекламы содержимое страницы доступно")
    @allure.severity(allure.severity_level.NORMAL)
    def test_page_content_after_closing_ad(self, ads_page):
        ads_page.wait_for_ad()
        ads_page.ad.close()
        assert "Do you love watching ads" in ads_page.description_text

    @allure.title("После закрытия рекламы ссылка на видео-инструкцию доступна")
    @allure.severity(allure.severity_level.MINOR)
    def test_guide_link_after_closing_ad(self, ads_page):
        ads_page.wait_for_ad()
        ads_page.ad.close()
        assert ads_page.is_guide_link_clickable()
        assert "youtube.com" in ads_page.guide_link_href


@allure.epic("Practice Automation")
@allure.feature("Рекламные окна")
@pytest.mark.negative
class TestAdsNegative:

    @allure.title("Реклама не показывается сразу после загрузки страницы")
    @allure.severity(allure.severity_level.NORMAL)
    def test_ad_not_shown_immediately(self, ads_page):
        assert not ads_page.is_ad_displayed_now()

    @allure.title("Реклама не появляется повторно сразу после закрытия")
    @allure.severity(allure.severity_level.NORMAL)
    def test_ad_not_reappearing_after_close(self, ads_page):
        ads_page.wait_for_ad()
        ads_page.ad.close()
        assert not ads_page.ad.is_open(timeout=3)

    @allure.title("Вместе с рекламой не открываются другие модальные окна")
    @allure.severity(allure.severity_level.MINOR)
    def test_other_modals_closed_while_ad_shown(self, ads_page):
        ads_page.wait_for_ad()
        assert ads_page.are_other_modals_hidden()
