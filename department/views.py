from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from .models import Department
from .forms import DepartmentModelForm
from accounts.decorators import admin_user
from django.shortcuts import get_object_or_404


from django.views.generic import ListView, DeleteView, UpdateView, CreateView, DetailView


@method_decorator(admin_user, name='dispatch')
class AllDepartment(ListView):
    paginate_by = 5
    model = Department
    template_name = 'department/list.html'


@method_decorator(admin_user, name='dispatch')
class DepartmentDetailView(DetailView):
    template_name = "department/department_detail.html"

    def get_object(self):
        id_ = self.kwargs.get("department_id")
        return get_object_or_404(Department, id=id_)


@method_decorator(admin_user, name='dispatch')
class DepartmentCreateView(CreateView):
    template_name = 'department/department_create.html'
    queryset = Department.objects.all()
    form_class = DepartmentModelForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        if not obj.created_by_id:
            obj.created_by_id = self.request.user.username
        obj.save()
        return redirect(obj.get_absolute_url())


@method_decorator(admin_user, name='dispatch')
class DepartmentUpdateView(UpdateView):
    template_name = 'department/department_create.html'
    form_class = DepartmentModelForm

    def get_object(self):
        department_id_ = self.kwargs.get('department_id')
        return get_object_or_404(Department, id=department_id_)

    def form_valid(self, form):
        obj = form.save(commit=False)
        if not obj.created_by_id:
            obj.created_by_id = self.request.user.username
        obj.save()
        return redirect(obj.get_absolute_url())


@method_decorator(admin_user, name='dispatch')
class DepartmentDeleteView(DeleteView):
    template_name = 'department/department_delete.html'
    success_url = "/department/"

    def get_object(self):
        department_id_ = self.kwargs.get('department_id')
        return get_object_or_404(Department, id=department_id_)

    def get_context_data(self, **kwargs):
        context = {}
        department_id_ = self.kwargs.get('department_id')
        if department_id_:
            from accounts.models import User
            context["total_user_in_department"] = User.objects.filter(department_id=department_id_).count()
        context.update(kwargs)
        return super().get_context_data(**context)
