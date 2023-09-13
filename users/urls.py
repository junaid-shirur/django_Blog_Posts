from django.urls import path
from .views import register_user, LoginView, UserView


urlpatterns = [
    path("register", register_user),
    path("login",LoginView.as_view()),
    path("user",UserView),
]