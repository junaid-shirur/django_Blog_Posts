from django.urls import path
from .views import getServices


urlpatterns = [
    path("services", getServices),
]