"""Sends a notification email when a visitor uses the portfolio chat's /message
command, plus a simple in-memory rate limiter to keep it from being spammed.
"""

import os
import smtplib
import time
from email.mime.text import MIMEText

from data import PROFILE

GMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

RATE_LIMIT_MAX = 3
RATE_LIMIT_WINDOW_SECONDS = 3600

_rate_limit_log: dict[str, list[float]] = {}


def is_rate_limited(ip: str) -> bool:
    """True if `ip` has already sent RATE_LIMIT_MAX messages within the window.

    Purely in-memory - resets on process restart, which is fine for a
    low-traffic personal site (a persistent store would be overkill here).
    """
    now = time.time()
    recent = [t for t in _rate_limit_log.get(ip, []) if now - t < RATE_LIMIT_WINDOW_SECONDS]
    if len(recent) >= RATE_LIMIT_MAX:
        _rate_limit_log[ip] = recent
        return True
    recent.append(now)
    _rate_limit_log[ip] = recent
    return False


def send_notification_email(text: str) -> None:
    msg = MIMEText(text)
    msg["Subject"] = "New message from your portfolio chat"
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = PROFILE["email"]

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, [PROFILE["email"]], msg.as_string())
