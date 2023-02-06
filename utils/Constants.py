from enum import Enum

class Enums(Enum):
    @classmethod
    def values(cls):
        return [member.value for member in cls]


DEFAULT_COUNTRY_CODE = '+91'
LOGIN_URL = "accounts:user-login"


USER_ROLE_CHOICE = (
    (1, 'Admin'),
    (2, 'User'),
)

class UserRoleChoice(Enums):
    Admin = 1
    User = 2

TICKET_PRIORITY = (
    ("Low", "Low"),
    ("Normal", "Normal"),
    ("High", "High"),
    ("Urgent", "Urgent"),
)


class TicketPriority(Enums):
    Low = "Low"
    Normal = "Normal"
    High = "High"
    Urgent = "Urgent"

ZENDESK_SUB_DOMAIN = "ghanhelp"
ZENDESK_API_TOKEN = "bWFpbHRvZ2hhbnNoeWFtNDdAZ21haWwuY29tL3Rva2VuOmdDRmNjTTJLV2x5TEN1M1Y3U29zU0NTNTdhTTBLendMdG9Ed1hpUVc"
ZENDESK_API_URLS = {
    "create": f'https://{ZENDESK_SUB_DOMAIN}.zendesk.com/api/v2/tickets',
    "delete": f'https://{ZENDESK_SUB_DOMAIN}.zendesk.com/api/v2/tickets/',
}


