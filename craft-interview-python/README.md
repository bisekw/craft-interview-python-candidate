# Framework testowy

Folder `craft-interview-python` zawiera szkielet testów, Page Objects i gotowe fixtures.

## Struktura i przeznaczenie plików

Poniżej struktura samego frameworka. Oznaczenie `[zadanie]` wskazuje pliki do uzupełnienia przez kandydata.

```text
craft-interview-python/
├── README.md                   opis struktury frameworka
├── TASKS.md                    polecenia i podział czasu rozmowy
├── config.py                   adres aplikacji, dane demo i czasy oczekiwania
├── conftest.py                 fixtures, przeglądarka i screenshoty błędów UI
├── requirements.txt            odwołanie do wspólnej listy zależności testów
├── pages/                      Page Objects: obsługa elementów strony
│   ├── __init__.py             oznaczenie pakietu Python
│   ├── base_page.py            gotowe operacje na UI z oczekiwaniem
│   └── login_page.py           locatory i obsługa logowania [zadanie]
└── tests/                      scenariusze oraz asercje
    ├── test_environment.py     gotowe sprawdzenia aplikacji i Chrome
    ├── test_ui.py              test logowania przez przeglądarkę [zadanie]
    └── test_api.py             test odpowiedzi API [zadanie]
```

## Jak współpracują elementy frameworka

Test UI korzysta z `LoginPage`, który dziedziczy gotowe operacje z `BasePage`. Page Object odpowiada za obsługę strony, a test za scenariusz i sprawdzenie wyniku. Test API wysyła żądania HTTP bez udziału Page Objectów.

Plik `conftest.py` w tym folderze przygotowuje obiekty używane przez testy. Takie obiekty nazywamy **fixtures**; pytest przekazuje je testom na podstawie nazw parametrów.

| Fixture | Co udostępnia |
|---|---|
| `base_url` | Adres aplikacji po sprawdzeniu jej dostępności. |
| `api_session` | Sesję HTTP do wysyłania żądań API. |
| `driver` | Przeglądarkę Chrome, zamykaną po teście. |
| `login_page` | Obiekt strony logowania korzystający z przeglądarki i adresu aplikacji. |

Podczas pracy we frameworku mogą pojawić się foldery `.cache/selenium/` z cache Selenium, `artifacts/` ze screenshotami błędów UI oraz `__pycache__/` z plikami generowanymi przez Pythona. Są pomijane przez Git.

## Zakres pracy kandydata

Polecenia znajdują się w [TASKS.md](TASKS.md).

Przygotowanie środowiska, wybór interpretera, instalacja zależności i uruchomienie testów są częścią oceny.

Część programistyczna obejmuje trzy pliki: `pages/login_page.py`, `tests/test_ui.py` i `tests/test_api.py`. Testy komunikują się z uruchomioną aplikacją przez HTTP.
