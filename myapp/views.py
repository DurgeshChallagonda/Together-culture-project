from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.http import HttpResponse, JsonResponse # type: ignore
from django.contrib.auth.forms import UserCreationForm # type: ignore
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout # type: ignore
from django.contrib.auth.models import User # type: ignore
from .models import Member, CustomUser  # Import CustomUser
from .serializers import RegisterSerializer
from rest_framework.renderers import JSONRenderer # type: ignore
from django.db.models import F  # Import F for database field updates
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, "home.html")

def register_member(request):  # Renamed from Member to register_member
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
        return redirect("/home")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

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

def change_membership(request, member_id):
    if request.method == 'POST':
        member = get_object_or_404(CustomUser, id=member_id)  # Use CustomUser instead of Member
        new_membership_type = request.POST.get('newMembershipType')
        if new_membership_type:
            member.membership_type = new_membership_type
            member.save()
            messages.success(request, 'Membership type updated successfully.')
        else:
            messages.error(request, 'Invalid membership type.')
        return redirect('admin_membership')  # Redirect to the admin membership page
    else:
        return redirect('admin_membership')  # Redirect if accessed via GET

def get_member_details(request, member_id):
    member = get_object_or_404(CustomUser, id=member_id)
    data = {
        'first_name': member.first_name,
        'last_name': member.last_name,
        'username': member.username,
        'email': member.email,
        'phone_number': member.phone_number,
        'interests': member.interests,
        'gender': member.gender,
        'date_of_birth': member.date_of_birth,
        'address': member.address,
    }
    return JsonResponse(data)

def edit_member(request, member_id):
    if request.method == 'POST':
        member = get_object_or_404(CustomUser, id=member_id)
        member.first_name = request.POST.get('first_name', member.first_name)
        member.last_name = request.POST.get('last_name', member.last_name)
        member.username = request.POST.get('username', member.username)
        member.email = request.POST.get('email', member.email)
        member.phone_number = request.POST.get('phone_number', member.phone_number)
        member.interests = request.POST.get('interests', member.interests)
        member.gender = request.POST.get('gender', member.gender)
        member.date_of_birth = request.POST.get('date_of_birth', member.date_of_birth)
        member.address = request.POST.get('address', member.address)
        member.save()
        messages.success(request, 'Member details updated successfully.')
        return redirect('admin_membership')
    return HttpResponse(status=405)