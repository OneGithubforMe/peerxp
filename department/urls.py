from django.contrib import admin
from django.urls import path, include
from .views import AllDepartment, DepartmentDetailView, DepartmentCreateView, DepartmentDeleteView, DepartmentUpdateView

app_name = "department"

urlpatterns = [
    path('', AllDepartment.as_view(), name="all-department"),
    path('create', DepartmentCreateView.as_view(), name="create-department"),
    path('<int:department_id>', DepartmentDetailView.as_view(), name="department-details"),
    path('<int:department_id>/update', DepartmentUpdateView.as_view(), name="update-department"),
    path('<int:department_id>/delete', DepartmentDeleteView.as_view(), name="delete-department")
]