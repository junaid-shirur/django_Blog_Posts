# Generated by Django 4.2.4 on 2023-09-15 19:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("virtual_queue", "0002_alter_services_service_details"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Service_Details",
        ),
        migrations.AlterField(
            model_name="services",
            name="service_details",
            field=models.TextField(),
        ),
    ]