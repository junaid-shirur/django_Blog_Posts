from django.contrib import admin

# Register your models here.
from .models import Services,Queue,Slot

admin.site.register(Services)
admin.site.register(Queue)
admin.site.register(Slot)


