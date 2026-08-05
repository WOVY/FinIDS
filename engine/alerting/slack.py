from pathlib import Path

import requests
import yaml

CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config" / "config.yaml"
CONFIG = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))["alerting"]


def send_slack_alert(alert: dict) -> bool:
    """config.yaml의 slack_webhook_url로 탐지 알림을 보낸다. webhook_url이 없으면 스킵."""
    webhook_url = CONFIG.get("slack_webhook_url", "")
    if not webhook_url:
        return False

    message = (
        f"*[FinIDS 탐지 알림]* {alert['rule_name']}\n"
        f"IP: {alert['ip']} / 계정: {alert.get('user_id') or '-'}\n"
        f"시각: {alert['triggered_at']}\n"
        f"{alert['description']}"
    )
    response = requests.post(webhook_url, json={"text": message}, timeout=10)
    return response.status_code == 200
