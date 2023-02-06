from django.db import models
from utils.Constants import TICKET_PRIORITY, TicketPriority
from department.models import Department
from django.urls import reverse

class ZendeskTicket(models.Model):
    zendesk_ticket_id = models.CharField(max_length=500, null=True, blank=True, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    subject = models.CharField(max_length=500)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=TICKET_PRIORITY, default=TicketPriority.Low.value)
    created_by = models.ForeignKey('accounts.user', on_delete=models.PROTECT, related_name="zendesk_ticket_created_by")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.subject}'

    def get_absolute_url(self):
        return reverse("ticket:ticket-all")