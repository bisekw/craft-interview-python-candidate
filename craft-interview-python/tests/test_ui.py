"""Zadanie 2: jeden krótki test poprawnego logowania przez LoginPage."""
import pytest
from config import VALID_USER, VALID_PASSWORD

pytestmark = pytest.mark.ui


@pytest.mark.parametrize("layout", ["normal", "reversed"])
def test_successful_login(login_page, layout):
    """Otwórz wskazany layout, zaloguj i sprawdź is_logged_in()."""
    raise NotImplementedError("Zadanie 2: test logowania UI")
