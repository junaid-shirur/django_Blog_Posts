# Generated by Django 4.2.4 on 2023-12-05 18:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Services",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True)),
                ("address", models.CharField(blank=True, max_length=100, null=True)),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                ("service_details", models.TextField(blank=True)),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[("open", "OPEN"), ("closed", "CLOSED")],
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Slot",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "slot",
                    models.CharField(
                        choices=[
                            ("morning", "Morning (9am-12pm)"),
                            ("noon", "Afternoon (12pm-3pm)"),
                            ("Evening", "Evening (4pm-8pm)"),
                        ],
                        default="morning",
                        max_length=50,
                    ),
                ),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                ("capacity", models.IntegerField(max_length=5)),
                ("request_number", models.IntegerField()),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="virtual_queue.services",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Queue",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("in_progress", "In Progress"),
                            ("completed", "Completed"),
                            ("canceled", "Canceled"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("date", models.DateField()),
                ("created_at", models.DateTimeField(auto_now=True)),
                ("updated_at", models.DateField(auto_now_add=True)),
                (
                    "slot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="virtual_queue.slot",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
