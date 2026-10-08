"""Gotowa konfiguracja — dane dotyczą wyłącznie lokalnej aplikacji demo."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE_URL = os.environ.get("QA_BASE_URL", "http://127.0.0.1:8000")
VALID_USER = "tester"
VALID_PASSWORD = "Interview123!"
TIMEOUT = 8
