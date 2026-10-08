# Python QA - zadanie na 40 minut

Jedno repozytorium zawiera gotową aplikację i szkielet testów w osobnych podfolderach. Sklonuj repozytorium i otwórz jego główny katalog w PyCharm lub swoim IDE.

## Uruchom aplikację

Wymagany jest zainstalowany Python 3.11+ dostępny w terminalu. Aplikacja korzysta wyłącznie ze standardowej biblioteki Pythona. Nie wymaga instalowania paczek ani przygotowywania środowiska testowego.

Z głównego katalogu repozytorium wykonaj **jedną komendę odpowiednią dla swojego systemu**.

Windows — PowerShell:

```powershell
.\start-app.cmd
```

macOS / Linux:

```sh
sh ./start-app.sh
```

Pozostaw terminal uruchomiony i otwórz http://127.0.0.1:8000. Login: `tester`, hasło: `Interview123!`. Zatrzymanie aplikacji: `Ctrl+C`.

Skrypt znajduje zainstalowanego Pythona i uruchamia tylko aplikację. Nie tworzy środowiska, nie instaluje zależności testowych i nie uruchamia testów. Jeśli nie znajdzie wymaganego Pythona, wyświetli czytelny komunikat.

Jeżeli port 8000 jest zajęty, dodaj `--port 8001` do komendy startowej i korzystaj z http://127.0.0.1:8001. Układ odwrócony strony jest dostępny pod `/?layout=reversed`.

## Twoje zadanie — środowisko testowe i testy

Otwórz drugi terminal w głównym katalogu tego samego repozytorium. Dalsze kroki wykonujesz samodzielnie:

- utwórz odizolowane środowisko Pythona dla testów;
- zainstaluj zależności opisane w głównym `requirements.txt` lub `pyproject.toml`;
- skonfiguruj interpreter IDE i sprawdź adres aplikacji używany przez testy;
- uruchom testy gotowości oznaczone markerem `ready`;
- uzupełnij zadania w [TASKS.md](craft-interview-python/TASKS.md).

Do testów UI wymagany jest Chrome. Pobranie paczek i pierwsze pobranie drivera wymagają Internetu. Konfiguracja środowiska jest częścią oceny. Samodzielnie dobierz komendy i wyjaśnij ich działanie.

Na starcie część testów zgłasza `NotImplementedError`, ponieważ ich uzupełnienie jest zadaniem. Gotowe są dwa testy sprawdzające aplikację i przeglądarkę.

## Struktura

```text
repozytorium/
├── start-app.cmd             uruchomienie aplikacji na Windows
├── start-app.sh              uruchomienie aplikacji na macOS / Linux
├── scripts/start-app.ps1     obsługa startu aplikacji na Windows
├── requirements.txt         zależności testów
├── pyproject.toml           metadane projektu i te same zależności testów
├── pytest.ini               konfiguracja pytest
├── qa-demo-app/              gotowa aplikacja HTTP i strona
└── craft-interview-python/   szkielet testów, Page Objects i zadania
```

Aplikacja i testy komunikują się przez HTTP. Nie potrzebujesz drugiego repozytorium, submodułów, Dockera ani BrowserStack. Główny `.gitignore` pomija środowiska, ustawienia IDE, cache i raporty.
