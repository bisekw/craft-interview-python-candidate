# Gotowa aplikacja do zadania QA

Aplikacja jest częścią tego samego repozytorium co szkielet testów. Uruchomienie opisano w [głównym README](../README.md).

Z głównego katalogu repozytorium:

Windows:

```powershell
.\start-app.cmd
```

macOS / Linux:

```sh
sh ./start-app.sh
```

Wymagany jest Python 3.11+. Aplikacja nie wymaga dodatkowych paczek ani środowiska testowego.

Otwórz http://127.0.0.1:8000. Login: `tester`, hasło: `Interview123!`. Zatrzymanie: `Ctrl+C`. Serwer nasłuchuje wyłącznie na `127.0.0.1`.

Interfejsy używane w zadaniu:

- `GET /health` → `200 {"status":"ok"}`.
- `GET /api/players/P-102` → `200`, obiekt `data` z danymi gracza.
- `POST /api/login` → obsługa logowania strony.

Kod aplikacji jest gotowy. Zadaniem kandydata jest przygotowanie środowiska testowego i uzupełnienie testów.
