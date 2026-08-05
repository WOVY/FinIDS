from engine.rules.abnormal_ua import AbnormalUARule
from engine.rules.base import Alert, Rule
from engine.rules.credential_stuffing import CredentialStuffingRule
from engine.rules.multi_account import MultiAccountRule
from engine.rules.night_transfer import NightTransferRule
from engine.rules.split_transfer import SplitTransferRule

ALL_RULES: list[Rule] = [
    CredentialStuffingRule(),
    NightTransferRule(),
    MultiAccountRule(),
    AbnormalUARule(),
    SplitTransferRule(),
]

__all__ = [
    "ALL_RULES",
    "Alert",
    "Rule",
    "CredentialStuffingRule",
    "NightTransferRule",
    "MultiAccountRule",
    "AbnormalUARule",
    "SplitTransferRule",
]
