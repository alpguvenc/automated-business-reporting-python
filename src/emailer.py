from __future__ import annotations

from email.message import EmailMessage
import mimetypes
import smtplib
from pathlib import Path


def send_email_with_attachment(
    *,
    smtp_host: str | None,
    smtp_port: int | None,
    username: str | None,
    password: str | None,
    email_from: str | None,
    email_to: str | None,
    subject: str,
    body: str,
    attachment_path: Path,
) -> None:
    if not all([smtp_host, smtp_port, username, password, email_from, email_to]):
        raise ValueError("SMTP/email settings are missing. Configure them in .env to enable email sending.")

    msg = EmailMessage()
    msg["From"] = email_from
    msg["To"] = email_to
    msg["Subject"] = subject
    msg.set_content(body)

    ctype, encoding = mimetypes.guess_type(str(attachment_path))
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)

    with open(attachment_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype=maintype,
            subtype=subtype,
            filename=attachment_path.name,
        )

    with smtplib.SMTP(smtp_host, int(smtp_port)) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(msg)
