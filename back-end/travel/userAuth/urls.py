from django.urls import path
from .views import login, register, user_profile

urlpatterns = [
    path("login/", login, name="login"),
    path("register/", register, name="register"),
    path(
        "user_profile/", user_profile, name="user_profile"
    ),  
]
