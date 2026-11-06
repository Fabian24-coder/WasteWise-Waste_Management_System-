from django.urls import path

from .web_views import register, web_login, web_logout

urlpatterns = [
    path("register/", register, name="web_register"),
    path("login/", web_login, name="web_login"),
    path("logout/", web_logout, name="web_logout"),
]
