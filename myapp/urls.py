from django.urls import path  # type: ignore
from . import views

print(dir(views))  # This will print all attributes of the views module

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
    path('member/dashboard/', views.member_dashboard, name='member_dashboard'),
    path('admin/event-control/', views.admin_event_control, name='admin_event_control'),
    path('admin/event/create/', views.create_event, name='create_event'),
    path('admin/event/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('membership/dashboard/', views.membership_dashboard, name='membership_dashboard'),
    path('membership/benefits/', views.membership_dashboard, name='membership_benefits'),
    path('event/book/<int:event_id>/', views.book_event, name='book_event'),
]