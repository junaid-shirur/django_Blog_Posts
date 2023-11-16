from django.urls import path
from .views import getServices, createService


urlpatterns = [
    path("services", getServices),
    path("create-service", createService),
]