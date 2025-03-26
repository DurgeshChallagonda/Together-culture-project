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
from django.shortcuts import render, redirect
from .models import Event
from .forms import EventForm
from .models import MembershipBenefit

from .forms import BookingForm


# Create your views here.

def admin_event_control(request):
    # Handle form submission for creating or editing events
    if request.method == 'POST':
        if 'event_id' in request.POST:  # Editing an event
            event = get_object_or_404(Event, id=request.POST['event_id'])
            form = EventForm(request.POST, instance=event)
        else:  # Creating a new event
            form = EventForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('admin_event_control')

    # Handle filtering
    category_filter = request.GET.get('category', None)
    if category_filter:
        events = Event.objects.filter(category=category_filter)
    else:
        events = Event.objects.all()

    # Initialize a blank form for new events
    form = EventForm()
    categories = Event.objects.values_list('category', flat=True).distinct()
    return render(request, 'AdminEventControl.html', {
        'events': events,
        'form': form,
        'categories': categories,
        'selected_category': category_filter,
    })

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
    # Handle event deletion
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('admin_event_control')
    return redirect('admin_event_control')

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
    events = Event.objects.all()  # Fetch all events from the database
    return render(request, 'MemberDashboard.html', {'events': events})

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_event_control')  # Redirect to the admin event control page
    else:
        form = EventForm()
    return render(request, 'AdminEventControl.html', {'form': form, 'events': Event.objects.all()})

def membership_dashboard(request):
    base_plan_benefits = MembershipBenefit.objects.filter(plan_type='Base')  # Base plan benefits
    upgraded_plan_benefits = MembershipBenefit.objects.filter(plan_type='Upgraded')  # Upgraded plan benefits
    return render(request, 'MembershipBreakdownBenefits.html', {
        'base_plan_benefits': base_plan_benefits,
        'upgraded_plan_benefits': upgraded_plan_benefits,
    })

def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.event = event
            booking.save()
            return redirect('member_dashboard')  # Redirect to the dashboard after booking
    else:
        form = BookingForm()
    return render(request, 'BookEvent.html', {'form': form, 'event': event})

class MembershipBenefit(models.Model):
    PLAN_CHOICES = [
        ('Base', 'Base Plan'),
        ('Upgraded', 'Upgraded Plan'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField()
    plan_type = models.CharField(max_length=50, choices=PLAN_CHOICES, default='Base')
    utilized = models.BooleanField(default=False)

    def __str__(self):
        return self.name