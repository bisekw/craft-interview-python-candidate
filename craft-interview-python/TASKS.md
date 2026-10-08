# Zadanie praktyczne — maksymalnie 40 minut

| Etap | Czas |
|---|---:|
| 0. Uruchomienie aplikacji i przygotowanie środowiska testowego | 8 min |
| 1. LoginPage: locatory i dwie metody | 10 min |
| 2. Test logowania UI | 7 min |
| 3. Prosty test GET API | 10 min |
| Omówienie kodu | 5 min |
| **Razem** | **40 min** |

Uruchom aplikację zgodnie z głównym README. Następnie samodzielnie przygotuj środowisko do testów — to część ocenianego zadania. Korzystaj z gotowych fixtures i BasePage. Część programistyczna obejmuje trzy wskazane pliki; nie budujesz dodatkowych modułów frameworka.

## 0. Środowisko testowe

1. Utwórz odizolowane środowisko Pythona dla testów.
2. Zainstaluj w nim zależności projektu opisane w głównym `requirements.txt` lub `pyproject.toml`.
3. Skonfiguruj interpreter w PyCharm lub swoim IDE i potwierdź, z którego środowiska korzystają testy.
4. Sprawdź, czy testy używają adresu uruchomionej aplikacji. Zmień go, jeśli jest niepoprawny, i uruchom gotowe testy oznaczone markerem `ready`.
5. Wyjaśnij, jak zachowasz środowisko lokalnie, a kod i opis zależności w Git.

Sposób wykonania i komendy dobierasz samodzielnie. Skrypt uruchomienia aplikacji nie przygotowuje środowiska testowego.

## 1. LoginPage — pages/login_page.py

Otwórz stronę z README i sprawdź DOM. Uzupełnij locatory w `LoginPage`:

- `USERNAME_INPUT` — pole loginu gracza.
- `PASSWORD_INPUT` — pole hasła gracza. ID tego pola zmienia się przy każdym załadowaniu strony.
- `LOGIN_BUTTON` — przycisk logowania gracza.
- `SUCCESS_MESSAGE` — komunikat wyniku logowania w formularzu gracza.

Dobór locatorów należy do Ciebie. Rozwiązanie ma działać po ponownym otwarciu strony i w obu dostępnych układach.

Uzupełnij dwie krótkie metody:

- `login(username, password)` — wpisz login, hasło i kliknij właściwy przycisk. Gotowy BasePage udostępnia `type_text(locator, value)` i `click(locator)` z oczekiwaniem.
- `is_logged_in()` — zwróć True, gdy w formularzu gracza widać komunikat `Zalogowano jako tester`. Możesz użyć `is_visible(locator)` i `text(locator)` z BasePage.

Nie dodawaj `sleep()`. `open_page(layout)` jest już gotowe.

## 2. Test UI — tests/test_ui.py

Napisz jeden test poprawnego logowania:

1. Otwórz stronę przez `login_page.open_page(layout)`.
2. Zaloguj danymi `VALID_USER` i `VALID_PASSWORD` z `config.py`.
3. Sprawdź wynik przez `is_logged_in()`. Dodaj czytelny komunikat asercji.

Gotowa parametryzacja wykona Twój test dla `normal` i `reversed`; nie piszesz drugiego testu. Fixture `login_page` tworzy Page Object i udostępnia przeglądarkę. Oczekiwana implementacja to kilka linijek.

## 3. Test API — tests/test_api.py

Napisz jeden test dla **GET `/api/players/P-102`**. Użyj gotowych `base_url` i `api_session`. Wywołaj żądanie z timeoutem.

Sprawdź:

1. Status HTTP to **200**.
2. JSON zawiera pole **data** będące obiektem.
3. **data.id** to **P-102**.
4. **data.email** kończy się na **@example.test**.

Dodaj czytelne komunikaty asercji. Przykładowy fragment odpowiedzi: `{"data":{"id":"P-102","email":"ala.nova@example.test", ...}}`. Nie tworzysz kont, nie zapisujesz danych i nie piszesz cleanup API.

## Omówienie — 5 minut

Wyjaśnij dobór locatorów, sposób oczekiwania na komunikat oraz znaczenie asercji API. Powiedz, co sprawdziłeś wykonaniem i gdzie skorzystałeś z podpowiedzi. Koniec po 40 minutach — bez zadań dodatkowych.
