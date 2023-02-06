from django.forms import ModelForm
from .models import ZendeskTicket

class ZendeskTicketModelForm(ModelForm):
    class Meta:
        model = ZendeskTicket
        fields = ('department', 'subject', 'description', 'priority')