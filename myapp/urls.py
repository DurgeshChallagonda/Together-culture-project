from django.urls import path  # type: ignore
from . import views
<<<<<<< Updated upstream

print(dir(views))  # This will print all attributes of the views module
=======
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
>>>>>>> Stashed changes

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),  # Ensure the correct view is referenced
    path("login/", views.customuser_login, name="customuser_login"),
    path("register.html", views.Register_view, name="register_html"),
    path("login.html", views.login, name="login_html"),
    path("member/register", views.Member, name="register"),
    path("member/login", views.member_login, name="member_login"),
    path("admin/login", views.admin_login, name="admin_login"),
    path("adminlogin.html", views.admin_login, name="admin_login"),
    path("user/", views.user, name="user"),
    path("print_register/", views.print_register, name="print_register"),
<<<<<<< Updated upstream
    # Remove or comment out the following line if the view does not exist
    path('member/dashboard/', views.member_dashboard, name='member_dashboard'),
    path('admin/event-control/', views.admin_event_control, name='admin_event_control'),
    path('admin/event/create/', views.create_event, name='create_event'),
    path('admin/event/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('membership/dashboard/', views.membership_dashboard, name='membership_dashboard'),
    path('membership/benefits/', views.membership_dashboard, name='membership_benefits'),
    path('event/book/<int:event_id>/', views.book_event, name='book_event'),
]
=======
    path("custom-admin-dashboard/", views.custom_admin_dashboard, name="custom_admin_dashboard"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("resources.html", views.resources, name="resources"),
    path("membership_plans.html", views.membership_plans, name="membership_plans"),
    path("custom-admin-dashboard/admin_members.html", views.admin_members, name="admin_members"),
    path("custom-admin-dashboard/admin_control_membership.html", views.admin_control_membership, name="admin_control_membership"),
    path("custom-admin-dashboard/admin/membership/", views.admin_membership, name="admin_membership"),
    path("change-membership/<int:member_id>/", views.change_membership, name="change_membership"),
    path("get-member-details/<int:member_id>/", views.get_member_details, name="get_member_details"),
    path("edit-member/<int:member_id>/", views.edit_member, name="edit_member"),
    path("add-member/", views.add_member, name="add_member"),
    path("membership/dashboard/", views.membership_dashboard, name="membership_dashboard"),
    path("membership/benefits/", views.membership_benefits, name="membership_benefits"),
    path("event/book/<int:event_id>/", views.book_event, name="book_event"),
    path("member/logout/", views.member_logout, name="member_logout"),
    path("custom-admin/event-control/", views.admin_event_control, name="admin_event_control"),
    path("custom-admin-dashboard/admin/event/create/", views.create_event, name="create_event"),
    path("custom-admin-dashboard/admin/event/delete/<int:event_id>/", views.delete_event, name="delete_event"),
    path('custom-admin-dashboard/admin/event/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('member/', views.member_dashboard, name='member'),
    path("member/dashboard/", views.member_dashboard, name="member_dashboard"),
    path('member/login', views.customuser_login, name='customuser_login'),
    path("member/profile/", views.view_profile, name="view_profile"),
    path("member/profile/edit/", views.edit_profile, name="edit_profile"),
    path('delete-member/<int:member_id>/', views.delete_member, name='delete_member'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('events/categories/', views.events_by_category, name='events_by_category'),
    path('add-to-user-events/', views.add_to_user_events, name='add_to_user_events'),
    path("my-events/", views.my_events, name="my_events"),
    path('event/<int:event_id>/', views.event_details, name='event_details'),
    path('membership/status/', views.membership_status, name='membership_status'),
    path('custom-admin-dashboard/admin_membershiptypes/', views.admin_membershiptypes, name='admin_membershiptypes'),
    path('add-membership/', views.add_membership, name='add_membership'),
    path('membership/<int:membership_id>/benefits/', views.manage_membership_benefits, name='manage_membership_benefits'),
    path('manage-benefits/', views.manage_all_benefits, name='manage_all_benefits'),
    path("request_upgrade/", views.request_upgrade, name="request_upgrade"),
    path("approve-upgrade/<int:request_id>/", views.approve_upgrade, name="approve_upgrade"),
    path("deny-upgrade/<int:request_id>/", views.deny_upgrade, name="deny_upgrade"),
    path('manage-courses/', views.manage_courses, name='admin_course_control'),
    path('custom-admin-dashboard/admin/course/create/', views.create_course, name='create_course'),
    path('custom-admin-dashboard/admin/course/edit/<int:course_id>/', views.edit_course, name='edit_course'),
    path('custom-admin-dashboard/admin/course/delete/<int:course_id>/', views.delete_course, name='delete_course'),
    path('course-modules/', views.course_modules, name='course_modules'),
    path('join-course/<int:course_id>/', views.join_course, name='join_course'),
    path('get_course_details/', views.get_course_details, name='get_course_details'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> Stashed changes
