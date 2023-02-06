from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class Department(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField()
    created_by = models.ForeignKey('accounts.user', on_delete=models.PROTECT, related_name="departement_created_by")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("department:department-details", kwargs={'department_id': self.id})
