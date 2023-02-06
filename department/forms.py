from django.forms import ModelForm
from .models import Department


class DepartmentModelForm(ModelForm):
    class Meta:
        model = Department
        fields = ('name', 'description')
