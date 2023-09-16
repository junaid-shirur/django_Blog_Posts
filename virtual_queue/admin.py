from django.contrib import admin

# Register your models here.
from .models import Services,Queue

admin.site.register(Services)
admin.site.register(Queue)
