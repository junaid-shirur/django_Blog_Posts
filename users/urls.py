from django.urls import path
from .views import register_user, login, getUser


urlpatterns = [
    path("register", register_user),
    path("login",login),
    path("user",getUser),
]