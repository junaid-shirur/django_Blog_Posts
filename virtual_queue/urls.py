from django.urls import path
from .views import getServices, createService,joinQueue, exitQueue


urlpatterns = [
    path("services", getServices),
    path("create-service", createService),
    path("join_queue", joinQueue),
    path("exit_queue",exitQueue)
]