from django.urls import path
from .views import getServices, createService,joinQueue


urlpatterns = [
    path("services", getServices),
    path("create-service", createService),
    path("join_queue", joinQueue)
]