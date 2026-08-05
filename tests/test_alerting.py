from unittest.mock import MagicMock

from engine.alerting.email import send_email_alert
from engine.alerting.slack import send_slack_alert

SAMPLE_ALERT = {
    "rule_name": "night_transfer",
    "ip": "10.0.0.1",
    "user_id": "user_002",
    "triggered_at": "2026-06-16T02:30:00Z",
    "description": "새벽 시간대 5,000,000원 고액 이체",
}


class TestSlackAlert:
    def test_sends_to_webhook_url(self, mock_slack, monkeypatch):
        monkeypatch.setattr(
            "engine.alerting.slack.CONFIG",
            {"slack_webhook_url": "https://hooks.slack.com/test"},
        )

        result = send_slack_alert(SAMPLE_ALERT)

        assert result is True
        mock_slack.assert_called_once()
        args, _ = mock_slack.call_args
        assert args[0] == "https://hooks.slack.com/test"

    def test_skips_when_webhook_url_empty(self, mock_slack, monkeypatch):
        monkeypatch.setattr("engine.alerting.slack.CONFIG", {"slack_webhook_url": ""})

        result = send_slack_alert(SAMPLE_ALERT)

        assert result is False
        mock_slack.assert_not_called()


class TestEmailAlert:
    def test_sends_via_gmail_smtp(self, monkeypatch):
        monkeypatch.setattr("engine.alerting.email.CONFIG", {"gmail_from": "test@gmail.com"})
        monkeypatch.setenv("GMAIL_APP_PASSWORD", "fake-app-password")

        smtp_instance = MagicMock()
        smtp_instance.__enter__.return_value = smtp_instance
        monkeypatch.setattr("smtplib.SMTP", MagicMock(return_value=smtp_instance))

        result = send_email_alert(SAMPLE_ALERT)

        assert result is True
        smtp_instance.starttls.assert_called_once()
        smtp_instance.login.assert_called_once_with("test@gmail.com", "fake-app-password")
        smtp_instance.send_message.assert_called_once()

    def test_skips_without_credentials(self, monkeypatch):
        monkeypatch.setattr("engine.alerting.email.CONFIG", {"gmail_from": ""})
        monkeypatch.delenv("GMAIL_APP_PASSWORD", raising=False)

        result = send_email_alert(SAMPLE_ALERT)

        assert result is False
