"""Gotowe, małe operacje na UI. Bez implicit wait i bez tłumienia awarii drivera."""

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver, base_url, timeout=8):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, timeout)

    def open(self, path="/"):
        self.driver.get(f"{self.base_url}{path}")

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type_text(self, locator, value):
        element = self.find(locator)
        element.clear()
        element.send_keys(str(value))

    def text(self, locator):
        return self.find(locator).text

    def is_visible(self, locator, timeout=2):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
