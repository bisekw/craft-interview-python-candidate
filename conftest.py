"""Opcje dostępne przy uruchamianiu pytest z głównego katalogu projektu."""
from config import BASE_URL


def pytest_addoption(parser):
    parser.addoption("--headed", action="store_true", help="Pokaż okno Chrome")
    parser.addoption("--base-url", default=BASE_URL, help="Adres uruchomionej aplikacji")
