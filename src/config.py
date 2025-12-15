from __future__ import annotations

from dataclasses import dataclass
import os
from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    api_base_url: str
    api_key: str
    api_timeout_seconds: int

    report_currency: str

    smtp_host: str | None
    smtp_port: int | None
    smtp_username: str | None
    smtp_password: str | None
    email_from: str | None
    email_to: str | None


def _get_int(name: str, default: int) -> int:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        raise ValueError(f"{name} must be an integer, got: {raw}")


def load_settings() -> Settings:
    load_dotenv()

    api_base_url = os.getenv("API_BASE_URL", "").strip()
    api_key = os.getenv("API_KEY", "").strip()

    if not api_base_url:
        raise ValueError("API_BASE_URL is missing in .env")
    if not api_key:
        raise ValueError("API_KEY is missing in .env")

    return Settings(
        api_base_url=api_base_url,
        api_key=api_key,
        api_timeout_seconds=_get_int("API_TIMEOUT_SECONDS", 20),
        report_currency=os.getenv("REPORT_CURRENCY", "USD"),
        smtp_host=os.getenv("SMTP_HOST") or None,
        smtp_port=_get_int("SMTP_PORT", 587) if os.getenv("SMTP_HOST") else None,
        smtp_username=os.getenv("SMTP_USERNAME") or None,
        smtp_password=os.getenv("SMTP_PASSWORD") or None,
        email_from=os.getenv("EMAIL_FROM") or None,
        email_to=os.getenv("EMAIL_TO") or None,
    )
