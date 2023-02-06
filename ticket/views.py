from accounts.decorators import login_user
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, HttpResponse, Http404
from .models import ZendeskTicket
from .forms import ZendeskTicketModelForm
from accounts.decorators import admin_user
from django.views.generic import ListView, DeleteView, CreateView, DetailView


@method_decorator(login_user, name='dispatch')
class ZendeskCreateView(CreateView):
    template_name = 'ticket/zendesk_ticket_create.html'
    queryset = ZendeskTicket.objects.all()
    form_class = ZendeskTicketModelForm

    def form_valid(self, form):
        ticket_obj = form.save(commit=False)
        if not ticket_obj.created_by_id:
            ticket_obj.created_by_id = self.request.user.username
        ticket_obj.save()
        from ticket.zendesk import Zendesk
        Zendesk.zendesk_create_api(ticket_obj)
        return redirect(ticket_obj.get_absolute_url())


@method_decorator(login_user, name='dispatch')
class AllZendeskTicketsView(ListView):
    paginate_by = 5
    model = ZendeskTicket
    template_name = 'ticket/list.html'

    def get_queryset(self):
        from utils.Constants import UserRoleChoice
        if self.request.user.role == UserRoleChoice.Admin.value:
            result = ZendeskTicket.objects.all()
        else:
            result = ZendeskTicket.objects.filter(created_by=self.request.user)
        return result


@method_decorator(admin_user, name='dispatch')
class DeleteZendeskTicketView(DeleteView):
    template_name = 'ticket/ticket_delete.html'
    success_url = "/ticket/"

    def get_object(self):
        ticket_id_ = self.kwargs.get('ticket_id')
        result = ZendeskTicket.objects.filter(id=ticket_id_).first()
        if not result:
            raise Http404("Not exist")
        return result

    def get_success_url(self):
        ticket_obj = self.get_object()
        if ticket_obj.zendesk_ticket_id:
            from ticket.zendesk import Zendesk
            Zendesk.delete_zendesk_ticket(ticket_obj.zendesk_ticket_id)
        return self.success_url


@method_decorator(login_user, name='dispatch')
class TicketDetailView(DetailView):
    template_name = "ticket/ticket_detail.html"

    def get_object(self):
        ticket_id_ = self.kwargs.get('ticket_id')
        from utils.Constants import UserRoleChoice

        result = ZendeskTicket.objects.filter(id=ticket_id_).first()
        if (not result) or (not (self.request.user.role == UserRoleChoice.Admin.value or self.request.user == result.created_by)):
            raise Http404("Not exist")
        return result

    def get_context_data(self, object):
        from ticket.zendesk import Zendesk
        is_successful, zendesk_data = Zendesk.get_zendesk_ticket_detail(object.zendesk_ticket_id)
        context = {
            "object": object,
            "zendesk_data": zendesk_data,
        }
        return super().get_context_data(**context)
