from django.urls import path  # type: ignore
from . import views

urlpatterns = [
    path ("", views.home, name="home"),
    path ("register/register.html", views.Member, name="register"),
    path ("register/login.html", views.login, name="login"),
    path("login.html", views.user, name="user"),
    path("member/register", views.Member, name="register"),
    path("member/login", views.member_login, name="member_login"),
    path("admin/login", views.admin_login, name="admin_login"),
    path("user/", views.user, name="user"),
    path("register", views.Member, name="register"),
    path("print_register/", views.print_register, name="print_register"),
]