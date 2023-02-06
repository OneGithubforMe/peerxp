# Generated by Django 4.1.5 on 2023-02-06 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ticket", "0003_remove_zendeskticket_updated_at_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="zendeskticket", name="priority",),
        migrations.AddField(
            model_name="zendeskticket",
            name="prioritys",
            field=models.CharField(
                choices=[
                    ("Low", "Low"),
                    ("Normal", "Normal"),
                    ("High", "High"),
                    ("Urgent", "Urgent"),
                ],
                default="Low",
                max_length=20,
            ),
        ),
    ]