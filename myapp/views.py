from django.shortcuts import render, redirect # type: ignore
from django.http import HttpResponse # type: ignore
from django.contrib.auth.forms import UserCreationForm # type: ignore
from django.contrib.auth import login, authenticate # type: ignore
from django.contrib.auth.models import User # type: ignore
from .models import Member,User
from .serializers import RegisterSerializer
from rest_framework.renderers import JSONRenderer # type: ignore
# Create your views here.
def home(request):
    return render(request, "home.html")

def Member(response):
    if response.method == "POST":
        form = UserCreationForm(response.POST)
        if form.is_valid():
            user=form.save()
        return redirect("/home")
    else:
      form = UserCreationForm()
    return render(response, "register.html" ,{"form":form })

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
    return render(request, "adminlogin.html")

def member_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/member/dashboard")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "member.html")

def print_register(request):
    items = Member.objects.all()
    serializer = RegisterSerializer(items, many=True)
    json_data = JSONRenderer().render(serializer.data)
    print(json_data)
    return HttpResponse(json_data, content_type="application/json")
    