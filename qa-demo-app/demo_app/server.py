import argparse
import json
import os
import secrets
import threading
from contextlib import contextmanager
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit


AUTH_TOKEN = "local-interview-token"
MAX_BODY_BYTES = 64 * 1024
STATIC_FILE = Path(__file__).with_name("static") / "index.html"
INVALID_JSON_BODY = object()

PLAYERS = (
    {"id": "P-101", "name": "Ala Nowak", "brand": "aurora", "email": "ala.aurora@example.test", "active": True, "roles": ["player"], "nickname": "ala-a", "daily_limit": 50},
    {"id": "P-102", "name": "Ala Nowak", "brand": "nova", "email": "ala.nova@example.test", "active": True, "roles": ["player", "vip"], "nickname": None, "daily_limit": 75},
    {"id": "P-103", "name": "Jan Kowalski", "brand": "aurora", "email": "jan@example.test", "active": True, "roles": ["player"], "nickname": "janek", "daily_limit": 25},
)


class AppState:
    def __init__(self):
        self.lock = threading.RLock()
        self.accounts = {}
        self.sessions = set()
        self.account_sequence = 0

    def create_account(self, brand):
        with self.lock:
            self.account_sequence += 1
            account = {
                "id": f"A-{self.account_sequence:04d}-{secrets.token_hex(3)}",
                "brand": brand,
                "daily_limit": 50,
                "nickname": None,
            }
            self.accounts[account["id"]] = account
            return dict(account)


def make_handler(state):
    class RequestHandler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def handle(self):
            try:
                super().handle()
            except (ConnectionResetError, BrokenPipeError):
                # Zamknięcie karty/drivera może przerwać połączenie keep-alive.
                # Pozostałe wyjątki nadal trafiają do standardowej diagnostyki serwera.
                self.close_connection = True

        def log_message(self, format_, *args):
            return

        def _send(self, status, body=None, *, content_type="application/json; charset=utf-8", headers=None):
            if body is None:
                payload = b""
            elif content_type.startswith("application/json"):
                payload = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            else:
                payload = body.encode("utf-8") if isinstance(body, str) else body
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(payload)))
            for key, value in (headers or {}).items():
                self.send_header(key, value)
            self.end_headers()
            if payload:
                self.wfile.write(payload)

        def _json_body(self):
            raw_length = self.headers.get("Content-Length")
            try:
                length = int(raw_length or "0")
            except ValueError:
                self._send(HTTPStatus.BAD_REQUEST, {"code": "INVALID_JSON"})
                return INVALID_JSON_BODY
            if length < 0:
                self._send(HTTPStatus.BAD_REQUEST, {"code": "INVALID_JSON"})
                return INVALID_JSON_BODY
            if length > MAX_BODY_BYTES:
                self.rfile.read(min(length, MAX_BODY_BYTES + 1))
                if length > MAX_BODY_BYTES + 1:
                    self.close_connection = True
                self._send(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"code": "BODY_TOO_LARGE"})
                return INVALID_JSON_BODY
            try:
                return json.loads(self.rfile.read(length))
            except (UnicodeDecodeError, json.JSONDecodeError):
                self._send(HTTPStatus.BAD_REQUEST, {"code": "INVALID_JSON"})
                return INVALID_JSON_BODY

        def _session_id(self):
            for part in self.headers.get("Cookie", "").split(";"):
                key, separator, value = part.strip().partition("=")
                if separator and key == "interview_session":
                    return value
            return None

        def _authorized(self):
            if self.headers.get("Authorization") == f"Bearer {AUTH_TOKEN}":
                return True
            session_id = self._session_id()
            with state.lock:
                return session_id is not None and session_id in state.sessions

        def _discard_body(self):
            try:
                length = int(self.headers.get("Content-Length") or "0")
            except ValueError:
                length = 0
            if length < 0:
                self._send(HTTPStatus.BAD_REQUEST, {"code": "INVALID_JSON"})
                return False
            if length:
                self.rfile.read(min(length, MAX_BODY_BYTES + 1))
                if length > MAX_BODY_BYTES + 1:
                    self.close_connection = True
            return True

        def _require_auth(self):
            if self._authorized():
                return True
            if not self._discard_body():
                return False
            self._send(HTTPStatus.UNAUTHORIZED, {"code": "UNAUTHORIZED"})
            return False

        def do_GET(self):
            parsed = urlsplit(self.path)
            path = parsed.path
            if path == "/health":
                self._send(HTTPStatus.OK, {"status": "ok"})
                return
            if path == "/":
                self._send(HTTPStatus.OK, STATIC_FILE.read_bytes(), content_type="text/html; charset=utf-8")
                return
            if path == "/favicon.ico":
                self._send(HTTPStatus.NO_CONTENT, content_type="image/x-icon")
                return
            if path == "/api/players":
                query = parse_qs(parsed.query)
                brand = query.get("brand", [None])[0]
                if brand not in (None, "aurora", "nova"):
                    self._send(HTTPStatus.BAD_REQUEST, {"code": "INVALID_BRAND"})
                    return
                players = [dict(player) for player in PLAYERS if brand is None or player["brand"] == brand]
                self._send(HTTPStatus.OK, {"data": players})
                return
            if path.startswith("/api/players/"):
                player_id = path.removeprefix("/api/players/")
                player = next((dict(item) for item in PLAYERS if item["id"] == player_id), None)
                self._send(HTTPStatus.OK, {"data": player}) if player else self._send(HTTPStatus.NOT_FOUND, {"code": "NOT_FOUND"})
                return
            if path.startswith("/api/accounts/"):
                if not self._require_auth():
                    return
                account_id = path.removeprefix("/api/accounts/")
                with state.lock:
                    account = state.accounts.get(account_id)
                    body = dict(account) if account else None
                self._send(HTTPStatus.OK, body) if body else self._send(HTTPStatus.NOT_FOUND, {"code": "NOT_FOUND"})
                return
            self._send(HTTPStatus.NOT_FOUND, {"code": "NOT_FOUND"})

        def do_POST(self):
            path = urlsplit(self.path).path
            if path == "/api/login":
                body = self._json_body()
                if body is INVALID_JSON_BODY:
                    return
                if body != {"username": "tester", "password": "Interview123!"}:
                    self._send(HTTPStatus.UNAUTHORIZED, {"code": "INVALID_CREDENTIALS"})
                    return
                session_id = secrets.token_urlsafe(24)
                with state.lock:
                    state.sessions.add(session_id)
                self._send(
                    HTTPStatus.OK,
                    {"authenticated": True},
                    headers={"Set-Cookie": f"interview_session={session_id}; Path=/; HttpOnly; SameSite=Lax"},
                )
                return
            if path == "/api/logout":
                session_id = self._session_id()
                with state.lock:
                    state.sessions.discard(session_id)
                self._send(
                    HTTPStatus.NO_CONTENT,
                    headers={"Set-Cookie": "interview_session=; Path=/; Max-Age=0; HttpOnly; SameSite=Lax"},
                )
                return
            if path == "/api/accounts":
                if not self._require_auth():
                    return
                body = self._json_body()
                if body is INVALID_JSON_BODY:
                    return
                if not isinstance(body, dict) or body.get("brand") not in ("aurora", "nova"):
                    self._send(HTTPStatus.UNPROCESSABLE_ENTITY, {"code": "INVALID_ACCOUNT"})
                    return
                self._send(HTTPStatus.CREATED, state.create_account(body["brand"]))
                return
            suffix = "/deposit-limit"
            if path.startswith("/api/accounts/") and path.endswith(suffix):
                if not self._require_auth():
                    return
                account_id = path[len("/api/accounts/"):-len(suffix)]
                body = self._json_body()
                if body is INVALID_JSON_BODY:
                    return
                limit = body.get("daily_limit") if isinstance(body, dict) else None
                if isinstance(limit, bool) or not isinstance(limit, int) or limit <= 0:
                    self._send(HTTPStatus.UNPROCESSABLE_ENTITY, {"code": "INVALID_DAILY_LIMIT"})
                    return
                with state.lock:
                    account = state.accounts.get(account_id)
                    if account:
                        account["daily_limit"] = limit
                self._send(HTTPStatus.OK, {"daily_limit": limit}) if account else self._send(HTTPStatus.NOT_FOUND, {"code": "NOT_FOUND"})
                return
            if not self._discard_body():
                return
            self._send(HTTPStatus.NOT_FOUND, {"code": "NOT_FOUND"})

        def do_DELETE(self):
            path = urlsplit(self.path).path
            if not path.startswith("/api/accounts/"):
                self._send(HTTPStatus.NOT_FOUND, {"code": "NOT_FOUND"})
                return
            if not self._require_auth():
                return
            account_id = path.removeprefix("/api/accounts/")
            with state.lock:
                existed = state.accounts.pop(account_id, None) is not None
            self._send(HTTPStatus.NO_CONTENT) if existed else self._send(HTTPStatus.NOT_FOUND, {"code": "NOT_FOUND"})

    return RequestHandler


class AppServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = os.name != "nt"

    def get_request(self):
        connection, address = super().get_request()
        connection.settimeout(5)
        return connection, address


def create_server(host="127.0.0.1", port=0):
    state = AppState()
    server = AppServer((host, port), make_handler(state))
    server.timeout = 1
    return server


@contextmanager
def running_app():
    server = create_server()
    thread = threading.Thread(target=server.serve_forever, name="interview-demo-app", daemon=True)
    thread.start()
    host, port = server.server_address
    try:
        yield f"http://{host}:{port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)


def main():
    parser = argparse.ArgumentParser(description="Run the local interview demo application")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    try:
        server = create_server(port=args.port)
    except OSError as error:
        parser.exit(1, f"Cannot start the application on port {args.port}: {error}. "
                       "Choose an available port with --port.\n")
    print(f"Demo app available at http://127.0.0.1:{server.server_port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
