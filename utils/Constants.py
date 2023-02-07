from enum import Enum
from django.conf import settings

class ModifiedEnum(Enum):
    @classmethod
    def values(cls):
        return [member.value for member in cls]


DEFAULT_COUNTRY_CODE = '+91'
LOGIN_URL = "accounts:user-login"


USER_ROLE_CHOICE = (
    (1, 'Admin'),
    (2, 'User'),
)


class UserRoleChoice(ModifiedEnum):
    Admin = 1
    User = 2


TICKET_PRIORITY = (
    ("low", "low"),
    ("normal", "normal"),
    ("high", "high"),
    ("urgent", "urgent"),
)


class TicketPriority(ModifiedEnum):
    Low = "Low"
    Normal = "Normal"
    High = "High"
    Urgent = "Urgent"

ZENDESK_SUB_DOMAIN = settings.ENV_DICT.get("ZENDESK_SUB_DOMAIN")
ZENDESK_API_TOKEN = settings.ENV_DICT.get("ZENDESK_API_TOKEN")
ZENDESK_API_URL = f'https://{ZENDESK_SUB_DOMAIN}.zendesk.com/api/v2/tickets/'


