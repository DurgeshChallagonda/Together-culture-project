from django.shortcuts import render, redirect # type: ignore
from django.http import HttpResponse # type: ignore
from django.contrib.auth.forms import UserCreationForm # type: ignore
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout # type: ignore
from django.contrib.auth.models import User # type: ignore
from .models import Member, CustomUser  # Import CustomUser
from .serializers import RegisterSerializer
from rest_framework.renderers import JSONRenderer # type: ignore
from django.db.models import F  # Import F for database field updates

# Create your views here.
def home(request):
    return render(request, "home.html")

def Member(response):
    if response.method == "POST":
        form = UserCreationForm(response.POST)
        if form.is_valid():
            user = form.save()
        return redirect("/home")
    else:
        form = UserCreationForm()
    return render(response, "register.html", {"form": form})

def login(request):
    return render(request, "login.html")

def about_us(request):
    return render(request, "about_us.html")

def user(request):
    items = User.objects.all()
    return render(request, "login.html", {"user": items})

def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("custom_admin_dashboard")  # Redirect to custom admin dashboard
        else:
            return render(request, "adminlogin.html", {"error": "Invalid credentials"})
    return render(request, 'adminlogin.html')

def custom_admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    # Add custom logic here
    return render(request, 'admin_dashboard.html')

def admin_logout(request):
    if request.method == "POST":
        auth_logout(request)
        return redirect('admin_login')
    return HttpResponse(status=405)

def member_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("/member/dashboard")
        else:
            return render(request, "member.html", {"error": "Wrong username or password"})
    return render(request, "member.html")

def print_register(request):
    items = Member.objects.all()
    serializer = RegisterSerializer(items, many=True)
    json_data = JSONRenderer().render(serializer.data)
    print(json_data)
    return HttpResponse(json_data, content_type="application/json")

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login_html")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

def member_dashboard(request):
    return render(request, 'member_dashboard.html')

def resources(request):
    return render(request, 'resources.html')

def membership_plans(request):
    return render(request, 'membership_plans.html')

def admin_members(request):
    return render (request, 'admin_members.html')

def admin_control_membership(request):
    return render(request, 'admin_control_membership.html')

def admin_membership(request):
    membership_type = request.GET.get('membershipType', 'all')  # Get the filter value from the request
    search_query = request.GET.get('searchMember', '')  # Get the search query from the request

    if membership_type == 'all':
        members = CustomUser.objects.all()  # Fetch all users
    else:
        members = CustomUser.objects.filter(membership_type=membership_type)  # Filter by membership type

    if search_query:  # If a search query is provided
        members = members.filter(username__icontains=search_query)  # Filter by username (case-insensitive)

    return render(request, 'admin_membership.html', {'members': members})