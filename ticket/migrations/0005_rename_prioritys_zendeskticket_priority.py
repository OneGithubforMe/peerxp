# Generated by Django 4.1.5 on 2023-02-06 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ticket", "0004_remove_zendeskticket_priority_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="zendeskticket", old_name="prioritys", new_name="priority",
        ),
    ]