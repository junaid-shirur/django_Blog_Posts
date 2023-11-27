from django.db import models
from users.models import User
from datetime import datetime

# Create your models here.

# class Service_Details(models.Model):
#     name = models.CharField(max_length=100)
#     def __str__(self):
#         return self.name
from django.core.validators import MaxValueValidator

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

class QueueParticipant(models.Model):
    participant = models.ForeignKey(User,on_delete=models.CASCADE)
    queue = models.ForeignKey("Queue", on_delete=models.CASCADE)
    reservation_time = models.DateTimeField(auto_now_add=True)
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
    joined_at = models.DateTimeField(auto_now_add=True)
    exited_at = models.DateTimeField(null=True)

class Queue(models.Model):
    STATUS = (
        ("open","OPEN"),
        ("closed","CLOSED"),
        ("full","FULL"),
        )
    estimated_wait_time = models.PositiveIntegerField(blank=True)
    service = models.OneToOneField(Services, on_delete=models.CASCADE)
    current_wait_time = models.DateTimeField()
    max_capacity = models.IntegerField(validators=[MaxValueValidator(20)])
    queue_status = models.CharField(choices=STATUS, max_length=10, blank=True)
    current_queue_size = models.IntegerField(blank=True)
    participants = models.ManyToManyField(User, through=QueueParticipant)

    def __str__(self) -> str:
        return f"Queue for the service {self.service.name}"
    