import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.popup import Popup

CONTAINER = "//div[contains(@class, 'pum-container')]"


class AdPopup(Popup):
    def __init__(self, driver):
        super().__init__(driver, f"{CONTAINER}[contains(., 'I am an ad')]", "Реклама")
        self.greeting = (By.XPATH, f"{self.xpath}//*[normalize-space(text())='Hi']")

    def is_greeting_displayed(self):
        return self.is_displayed(self.greeting, 3)


class AdsPage(BasePage):
    path = "/ads/"

    HOME_LINK = (By.XPATH, "//a[normalize-space()='Home']")
    DESCRIPTION = (By.XPATH, "//p[contains(., 'Do you love watching ads')]")
    GUIDE_LINK = (By.XPATH, "//a[contains(normalize-space(), 'how to handle ads')]")
    SIMPLE_MODAL = (By.XPATH, f"{CONTAINER}[contains(., 'a simple modal')]")
    FORM_MODAL = (By.XPATH, f"{CONTAINER}[contains(., 'Please enter your contact info below')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.ad = AdPopup(driver)

    @allure.step("Дождаться появления рекламного окна")
    def wait_for_ad(self, timeout=20):
        return self.ad.is_open(timeout)

    def is_ad_displayed_now(self):
        return self.is_displayed(self.ad.container, 0)

    def is_home_link_displayed(self):
        return self.is_displayed(self.HOME_LINK, 3)

    @property
    def description_text(self):
        return self.visible(self.DESCRIPTION).text

    @property
    def guide_link_href(self):
        return self.find(self.GUIDE_LINK).get_attribute("href")

    def is_guide_link_clickable(self):
        return self.find(self.GUIDE_LINK).is_enabled() and self.is_displayed(self.GUIDE_LINK, 3)

    def are_other_modals_hidden(self):
        return self.is_hidden(self.SIMPLE_MODAL, 1) and self.is_hidden(self.FORM_MODAL, 1)
