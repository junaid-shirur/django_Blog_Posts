from django.db import models
from users.models import User
from datetime import datetime


class Slot(models.Model):
    slot = models.CharField(
        max_length=50,
        choices=[
            ('morning', 'Morning (9am-12pm)'),
            ('noon', 'Afternoon (12pm-3pm)'),
            ('Evening', 'Evening (4pm-8pm)'),
        ],
        default='morning',
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.IntegerField(max_length=5)
    request_number = models.IntegerField(default=1)
    service = models.ForeignKey("Services", on_delete=models.CASCADE)

class Services(models.Model):
    STATUS = (
        ("open","OPEN"),
        ("closed","CLOSED"))
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=100, null=True,blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    service_details = models.TextField(blank=True)
    status = models.CharField(choices=STATUS, blank=True, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    def current_status(self):
        current_time = datetime.now().time()
        if self.start_time <= current_time <= self.end_time:
            return "open"
        else:
            return "closed"
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        current_time = datetime.now().time()

        if self.start_time <= current_time <= self.end_time:
            self.status = "open"
        else:
            self.status = "closed"

        super().save(*args, **kwargs)

class Queue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('canceled', 'Canceled'),
        ],
        default='pending',
    )
    date = models.DateField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)

    