from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.http import HttpResponse # type: ignore
from django.contrib.auth.forms import UserCreationForm # type: ignore
from django.contrib.auth import login as auth_login, authenticate # type: ignore
from django.contrib.auth.models import User # type: ignore
from .models import Member
from .serializers import RegisterSerializer
from rest_framework.renderers import JSONRenderer # type: ignore
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event
from .forms import EventForm



# Create your views here.

def admin_event_control(request):
    events = Event.objects.all()
    return render(request, 'AdminEventControl.html', {'events': events})

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_event_control')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})

def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('admin_event_control')
    else:
        form = EventForm(instance=event)
    return render(request, 'edit_event.html', {'form': form})

def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('admin_event_control')
    return render(request, 'delete_event.html', {'event': event})

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
            return redirect("/admin/")  # Redirect to Django admin dashboard
        else:
            return render(request, "adminlogin.html", {"error": "Invalid credentials"})
    return render(request, 'adminlogin.html')

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
    return render(request, 'MemberDashboard.html')