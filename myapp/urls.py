from django.urls import path  # type: ignore
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("register.html", views.register, name="register_html"),
    path("login.html", views.login, name="login_html"),
    path("member/register", views.Member, name="register"),
    path("member/login", views.member_login, name="member_login"),
    path("admin/login", views.admin_login, name="admin_login"),
    path("adminlogin.html", views.admin_login, name="admin_login"),
    path("user/", views.user, name="user"),
    path("print_register/", views.print_register, name="print_register"),
    path('member/dashboard', views.member_dashboard, name='member_dashboard'),

    # new code
     path('course.html', TemplateView.as_view(template_name='course.html'), name='course'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]