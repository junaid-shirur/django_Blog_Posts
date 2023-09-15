from django.db import models

# Create your models here.

# class Service_Details(models.Model):
#     name = models.CharField(max_length=100)
#     def __str__(self):
#         return self.name


class Services(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    operating_hours = models.CharField(max_length=100)
    estimated_wait_time = models.PositiveIntegerField()
    service_details = models.TextField()

    def __str__(self):
        return self.name
