from django.urls import path, include  # type: ignore
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views
from myapp import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("register.html", views.register, name="register_html"),
    path("login.html", views.login, name="login_html"),
    path("about_us.html", views.about_us, name="about_us.html"),
    path("member/register", views.register_member, name="register"),  # Updated view name
    path("member/login", views.member_login, name="member_login"),
    path("admin/login", views.admin_login, name="admin_login"),
    path("adminlogin.html", views.admin_login, name="admin_login"),
    path("user/", views.user, name="user"),
    path("print_register/", views.print_register, name="print_register"),
    path("member/dashboard", views.member_dashboard, name='member_dashboard'),
    path("custom-admin-dashboard/", views.custom_admin_dashboard, name='custom_admin_dashboard'),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("resources.html", views.resources, name="resources"),
    path("membership_plans.html", views.membership_plans, name="membership_plans"),
    path("custom-admin-dashboard/admin_members.html", views.admin_members, name="admin_members"),
    path("custom-admin-dashboard/admin_control_membership.html", views.admin_control_membership, name="admin_control_membership"),
    path('custom-admin-dashboard/admin/membership/', views.admin_membership, name='admin_membership'),
    path('change-membership/<int:member_id>/', views.change_membership, name='change_membership'),
    path('get-member-details/<int:member_id>/', views.get_member_details, name='get_member_details'),
    path('edit-member/<int:member_id>/', views.edit_member, name='edit_member'),
]