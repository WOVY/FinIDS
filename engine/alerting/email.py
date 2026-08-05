import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

import yaml

CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config" / "config.yaml"
CONFIG = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))["alerting"]

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


def send_email_alert(alert: dict, to_addr: str | None = None) -> bool:
    """Gmail SMTP(STARTTLS)로 탐지 알림 이메일을 보낸다.

    gmail_from 또는 GMAIL_APP_PASSWORD 환경변수가 없으면 스킵한다.
    앱 비밀번호를 config.yaml에 두지 않는 이유는 자격증명을 git에 커밋하지 않기 위함이다.
    """
    from_addr = CONFIG.get("gmail_from", "")
    app_password = os.environ.get("GMAIL_APP_PASSWORD", "")
    if not from_addr or not app_password:
        return False

    message = EmailMessage()
    message["Subject"] = f"[FinIDS 탐지 알림] {alert['rule_name']}"
    message["From"] = from_addr
    message["To"] = to_addr or from_addr
    message.set_content(
        f"IP: {alert['ip']}\n"
        f"계정: {alert.get('user_id') or '-'}\n"
        f"시각: {alert['triggered_at']}\n"
        f"{alert['description']}"
    )

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(from_addr, app_password)
        server.send_message(message)
    return True
