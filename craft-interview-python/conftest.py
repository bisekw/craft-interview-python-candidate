"""Gotowa infrastruktura. Kandydat nie musi jej modyfikować."""
import logging
import os
import re
from uuid import uuid4

import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from config import ROOT, TIMEOUT


def pytest_report_header():
    return "Zadanie 40 minut: 3 pliki do uzupełnienia. -m ready sprawdza tylko instalację."


@pytest.fixture(scope="session")
def base_url(pytestconfig):
    """Testy używają niezależnie uruchomionej aplikacji przez HTTP."""
    url = pytestconfig.getoption("--base-url").strip().rstrip("/")
    try:
        with requests.Session() as session:
            session.trust_env = False
            response = session.get(f"{url}/health", timeout=3)
    except requests.RequestException:
        pytest.fail(
            f"Aplikacja nie odpowiada pod {url}. Uruchom .\\start-app.cmd (Windows) "
            "lub sh ./start-app.sh (macOS/Linux) z głównego katalogu repozytorium "
            "w osobnym terminalu albo podaj poprawny --base-url. Instrukcja: główny README.md.",
            pytrace=False,
        )
    try:
        healthy = response.status_code == 200 and response.json() == {"status": "ok"}
    except ValueError:
        healthy = False
    if not healthy:
        pytest.fail(f"Adres {url}/health nie zwraca oczekiwanego stanu aplikacji. Sprawdź --base-url.", pytrace=False)
    return url


@pytest.fixture
def api_session():
    with requests.Session() as session:
        session.trust_env = False
        yield session


@pytest.fixture
def driver(pytestconfig):
    cache = ROOT / ".cache" / "selenium"
    cache.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("SE_CACHE_PATH", str(cache))
    options = webdriver.ChromeOptions()
    if not pytestconfig.getoption("--headed"):
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1000")
    if os.environ.get("QA_BROWSER_BINARY"):
        options.binary_location = os.environ["QA_BROWSER_BINARY"]
    path = os.environ.get("QA_DRIVER_PATH")
    service = Service(executable_path=path) if path else Service()
    browser = webdriver.Chrome(options=options, service=service)
    try:
        browser.set_page_load_timeout(20)
        browser.implicitly_wait(0)
        yield browser
    finally:
        browser.quit()


@pytest.fixture
def login_page(driver, base_url):
    from pages.login_page import LoginPage

    return LoginPage(driver, base_url, timeout=TIMEOUT)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    result = yield
    report = result.get_result()
    browser = item.funcargs.get("driver")
    if not report.failed or report.when != "call" or browser is None:
        return
    try:
        folder = ROOT / "artifacts"
        folder.mkdir(exist_ok=True)
        name = re.sub(r"[^a-zA-Z0-9_-]", "_", item.name)[:70]
        target = folder / f"{name}-{uuid4().hex[:8]}.png"
        if not browser.save_screenshot(str(target)):
            raise OSError("Nie zapisano screenshotu")
        report.sections.append(("Screenshot", str(target)))
    except Exception as error:
        logging.getLogger(__name__).warning("Screenshot: %s", error)
