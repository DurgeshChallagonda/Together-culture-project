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
    path("adminlogin.html", views.admin_login, name="admin_login"),
    path("user/", views.user, name="user"),
    path("print_register/", views.print_register, name="print_register"),
    # Remove or comment out the following line if the view does not exist
    # path('member/dashboard', views.member_dashboard, name='member_dashboard'),
    path('admin/event-control/', views.admin_event_control, name='admin_event_control'),
    path('admin/event/create/', views.create_event, name='create_event'),
    path('admin/event/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('admin/event/delete/<int:event_id>/', views.delete_event, name='delete_event'),
]