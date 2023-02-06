from django.contrib import admin
from django.urls import path, include
from .views import ZendeskCreateView, AllZendeskTicketsView, DeleteZendeskTicketView, TicketDetailView#AllDepartment, DepartmentDetailView, DepartmentCreateView, DepartmentDeleteView, DepartmentUpdateView

app_name = "ticket"

urlpatterns = [
    path('', AllZendeskTicketsView.as_view(), name="ticket-all"),
    path('create', ZendeskCreateView.as_view(), name="ticket-create"),

    path('<int:ticket_id>', TicketDetailView.as_view(), name="ticket-details"),
    # path('<int:department_id>/update', DepartmentUpdateView.as_view(), name="update-department"),
    path('<int:ticket_id>/delete', DeleteZendeskTicketView.as_view(), name="ticket-delete")
]