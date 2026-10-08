"""Zadanie 1: uzupełnij locatory i dwie krótkie metody."""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME_INPUT = None  # TODO
    PASSWORD_INPUT = None  # TODO: ID pola zmienia się przy każdym załadowaniu strony.
    LOGIN_BUTTON = None  # TODO
    SUCCESS_MESSAGE = None  # TODO

    def open_page(self, layout="normal"):
        self.open(f"/?layout={layout}")

    def login(self, username: str, password: str):
        """Wpisz login, wpisz hasło i kliknij właściwy przycisk."""
        raise NotImplementedError("Zadanie 1: login")

    def is_logged_in(self) -> bool:
        """Zwróć True, gdy widoczny jest tekst: Zalogowano jako tester."""
        raise NotImplementedError("Zadanie 1: is_logged_in")
