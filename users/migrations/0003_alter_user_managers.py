# Generated by Django 4.2.4 on 2023-09-15 18:49

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_remove_user_name_alter_user_email_and_more"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[],
        ),
    ]