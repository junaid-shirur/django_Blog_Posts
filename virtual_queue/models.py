from django.db import models
from users.models import User
# Create your models here.

# class Service_Details(models.Model):
#     name = models.CharField(max_length=100)
#     def __str__(self):
#         return self.name


class Services(models.Model):
    STATUS = (
        ("open","OPEN"),
        ("closed","CLOSED"))
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, null=True,blank=True)
    operating_hours = models.CharField(max_length=100)
    estimated_wait_time = models.PositiveIntegerField(blank=True)
    service_details = models.TextField(blank=True)
    status = models.CharField(choices=STATUS, blank=True, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Queue(models.Model):
    STATUS = (
        ("open","OPEN"),
        ("closed","CLOSED"))
    estimated_wait_time = models.PositiveIntegerField(blank=True)
    service_ref = models.ForeignKey(Services, on_delete=models.CASCADE)
    current_wait_time = models.DateTimeField()
    max_capacity = models.IntegerField()
    queue_status = models.CharField(choices=STATUS, max_length=10, blank=True)
    current_queue_size = models.IntegerField(max_length=200)
    queue_start_time = models.DateTimeField()
    queue_end_time = models.DateTimeField()
    participants = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, null=True,blank=True)
    description = models.TextField(max_length=400, blank=True)

    def __str__(self) -> str:
        return self.service_ref.name