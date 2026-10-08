"""Gotowe sprawdzenia instalacji. Nie stanowią wyniku oceny kandydata."""

import pytest
from selenium.webdriver.common.by import By

pytestmark = pytest.mark.ready


def test_local_http_is_ready(base_url, api_session):
    response = api_session.get(f"{base_url}/health", timeout=5)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.ui
def test_real_browser_is_ready(driver, base_url):
    driver.get(base_url)
    assert driver.find_element(By.ID, "app-title").is_displayed()
