from django.shortcuts import render

from django.shortcuts import render, redirect
from django.views import View
from accounts.decorators import guest_user, login_user
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import redirect, HttpResponse, Http404
from .models import ZendeskTicket
from .forms import ZendeskTicketModelForm
from accounts.decorators import admin_user
from django.shortcuts import get_object_or_404


from django.views.generic import ListView, DeleteView, UpdateView, CreateView, DetailView


@method_decorator(login_user, name='dispatch')
class ZendeskCreateView(CreateView):
    template_name = 'ticket/zendesk_ticket_create.html'
    queryset = ZendeskTicket.objects.all()
    form_class = ZendeskTicketModelForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        if not obj.created_by_id:
            obj.created_by_id = self.request.user.username
        obj.save()
        self.zendesk_create_api(obj)
        return redirect(obj.get_absolute_url())

    def zendesk_create_api(self, obj):
        try:
            from utils.ExternalApiCall import ExternalApi
            from utils.Constants import ZENDESK_API_URLS, ZENDESK_API_TOKEN
            data = {
                "ticket": {
                    "comment": {
                        "body": obj.description
                    },
                    "priority": obj.priority,
                    "subject": obj.subject
                }
            }
            headers = {
                "Authorization": f"Basic {ZENDESK_API_TOKEN}"
            }
            is_successful, response = ExternalApi(url=ZENDESK_API_URLS["create"], data=data, headers=headers).post()
            if response.get('ticket'):
                obj.zendesk_ticket_id = response['ticket'].get('id')
                obj.save()
        except Exception as e:
            raise Http404(e)


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


@method_decorator(login_user, name='dispatch')
class DeleteZendeskTicketView(DeleteView):
    template_name = 'ticket/ticket_delete.html'
    success_url = "/ticket/"

    def get_object(self):
        ticket_id_ = self.kwargs.get('ticket_id')
        from utils.Constants import UserRoleChoice

        result = ZendeskTicket.objects.filter(id=ticket_id_).first()
        if (not result) or (self.request.user.role != UserRoleChoice.Admin.value and self.request.user == result.created_by):
            raise Http404("Not exist")
        return result

    def get_success_url(self):
        ticket_obj = self.get_object()
        if ticket_obj.zendesk_ticket_id:
            try:
                from utils.ExternalApiCall import ExternalApi
                from utils.Constants import ZENDESK_API_URLS, ZENDESK_API_TOKEN
                headers = {
                    "Authorization": f"Basic {ZENDESK_API_TOKEN}"
                }
                ExternalApi(url=f'{ZENDESK_API_URLS["delete"]}{ticket_obj.zendesk_ticket_id}', headers=headers).delete()
            except Exception as e:
                raise Http404(e)
        if self.success_url:
            return self.success_url
        else:
            raise Http404("No URL to redirect to. Provide a success_url.")


@method_decorator(login_user, name='dispatch')
class TicketDetailView(DetailView):
    template_name = "ticket/ticket_detail.html"

    def get_object(self):
        ticket_id_ = self.kwargs.get('ticket_id')
        from utils.Constants import UserRoleChoice

        result = ZendeskTicket.objects.filter(id=ticket_id_).first()
        if (not result) or (
                self.request.user.role != UserRoleChoice.Admin.value and self.request.user == result.created_by):
            raise Http404("Not exist")
        return result