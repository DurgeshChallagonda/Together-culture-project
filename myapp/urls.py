from django.urls import path  # type: ignore
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("register.html", views.register, name="register_html"),
    path("login.html", views.login, name="login_html"),
    path("member/register", views.Member, name="register"),
    path("member/login", views.member_login, name="member_login"),
    path("admin/login", views.admin_login, name="admin_login"),
    path("user/", views.user, name="user"),
    path("print_register/", views.print_register, name="print_register"),
]