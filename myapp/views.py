from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.db import IntegrityError
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import (
    CustomUser, Event, MembershipBenefit, Booking, Register, Profile, Member, Membership, MembershipUpgradeRequest, Course, Category
)
from .forms import EventForm, BookingForm, MembershipForm, CourseForm
from .serializers import RegisterSerializer
from rest_framework.renderers import JSONRenderer
import logging
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)

# Create your views here.
def home(request):
    return render(request, "home.html")

def register_member(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
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
            if user.is_staff:  # Ensure the user has staff permissions
                auth_login(request, user)
                return redirect("custom_admin_dashboard")  # Redirect to custom admin dashboard
            else:
                error_message = "You do not have the required permissions to access this page."
        else:
            error_message = "Invalid username or password. Please try again."
        return render(request, "adminlogin.html", {"error": error_message})
    return render(request, 'adminlogin.html')

def custom_admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    events = Event.objects.filter(date__gte=now()).order_by('date')[:3]
    memberships = Membership.objects.prefetch_related('benefits').all()  # Fetch memberships with benefits
    courses = Course.objects.all()
    return render(request, 'admin_dashboard.html', {
        'events': events,
        'memberships': memberships,
        'courses': courses,
    })

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

def member_logout(request):
    auth_logout(request)
    return redirect('member_login') 

def print_register(request):
    items = CustomUser.objects.all()  # Use CustomUser instead of Member
    serializer = RegisterSerializer(items, many=True)
    json_data = JSONRenderer().render(serializer.data)
    return HttpResponse(json_data, content_type="application/json")

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('Firstname')
        last_name = request.POST.get('Lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone_number = request.POST.get('PhoneNumber')
        gender = request.POST.get('Gender')
        date_of_birth = request.POST.get('DateOfBirth')
        address = request.POST.get('Address')
        interests = request.POST.get('Interests')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return redirect('register')

        try:
            # Automatically assign "Individual Membership"
            membership = Membership.objects.get(name="Individual Membership")

            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                phone_number=phone_number,
                gender=gender,
                date_of_birth=date_of_birth,
                address=address,
                membership_type=membership,
                interests=interests
            )
            user.set_password(password)  # Hash the password
            user.save()

            # Create a Member profile for the user
            Member.objects.create(user=user)

            messages.success(request, "Account created successfully!")
            return redirect('login')
        except Membership.DoesNotExist:
            messages.error(request, "Default membership type not found. Please contact support.")
            return redirect('register')
        except IntegrityError:
            messages.error(request, "An account with this username or email already exists.")
            return redirect('register')
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect('register')

    return render(request, 'register.html')

def resources(request):
    return render(request, 'resources.html')

def membership_plans(request):
    return render(request, 'membership_plans.html')

def admin_members(request):
    # Update the field name to match the actual relationship in the Member model
    members = Member.objects.filter(custom_user__is_superuser=False, custom_user__is_staff=False)  # Adjusted field name
    return render(request, 'admin_members.html', {'members': members})

def admin_control_membership(request):
    upgrade_requests = MembershipUpgradeRequest.objects.filter(is_verified=False).select_related('user')
    return render(request, 'admin_control_membership.html', {
        'upgrade_requests': upgrade_requests
    })

def admin_membership(request):
    User = get_user_model()  # Get the custom user model
    search_query = request.GET.get('searchMember', '')
    membership_type_filter = request.GET.get('membershipType', 'all')

    # Filter members based on search query
    members = User.objects.filter(
        Q(first_name__icontains=search_query) |
        Q(last_name__icontains=search_query) |
        Q(username__icontains=search_query) |
        Q(email__icontains=search_query)
    ).exclude(is_superuser=True)  # Ensure this parenthesis is closed

    # Apply membership type filter if not "all"
    if membership_type_filter != 'all':
        members = members.filter(membership_type=membership_type_filter)

    # Fetch all memberships for the dropdown
    memberships = Membership.objects.all()

    return render(request, 'admin_membership.html', {
        'members': members,
        'memberships': memberships,
    })

def change_membership(request, member_id):
    if request.method == 'POST':
        member = get_object_or_404(CustomUser, id=member_id)
        new_membership_name = request.POST.get('newMembershipType')
        new_membership_type = get_object_or_404(Membership, name=new_membership_name)  # Fetch the Membership instance
        member.membership_type = new_membership_type  # Assign the Membership instance
        member.save()
        messages.success(request, 'Membership type updated successfully.')
        return redirect('admin_membership')
    else:
        return redirect('admin_membership')

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

def add_member(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        interests = request.POST.get('interests')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        address = request.POST.get('address')
        membership_name = request.POST.get('membership_type')

        # Fetch the Membership instance
        membership_type = get_object_or_404(Membership, name=membership_name)

        # Create a new user with a default password
        new_member = CustomUser.objects.create_user(
            username=username,
            email=email,
            password='12345678',  # Default password
            first_name=first_name,
            last_name=last_name,
        )
        new_member.phone_number = phone_number
        new_member.interests = interests
        new_member.gender = gender
        new_member.date_of_birth = date_of_birth
        new_member.address = address
        new_member.membership_type = membership_type  # Assign the Membership instance
        new_member.save()

        return redirect('admin_membership')  # Redirect to the membership management page

    # Fetch all memberships for the dropdown
    memberships = Membership.objects.all()
    return render(request, 'add_member.html', {'memberships': memberships})

def admin_event_control(request):
    categories = Event.objects.values_list('category', flat=True).distinct()
    selected_category = request.GET.get('category', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    events = Event.objects.all()
    if selected_category:
        events = events.filter(category=selected_category)
    if start_date:
        events = events.filter(date__gte=start_date)
    if end_date:
        events = events.filter(date__lte=end_date)

    context = {
        'categories': categories,
        'selected_category': selected_category,
        'start_date': start_date,
        'end_date': end_date,
        'events': events,
    }
    return render(request, 'AdminEventControl.html', context)

def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)  # Ensure the event exists
    categories = Event.objects.values_list('category', flat=True).distinct()  # Fetch distinct categories
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)  # Include request.FILES
        if form.is_valid():
            if 'image' in request.FILES:  # Check if a new image is uploaded
                event.image = request.FILES['image']  # Save the uploaded image file
            form.save()  # Save the form, including the updated image
            return redirect('admin_event_control')
        else:
            messages.error(request, 'Failed to update the event. Please check the form for errors.')
    else:
        form = EventForm(instance=event)
    return render(request, 'edit_event.html', {
        'form': form,
        'event': event,
        'categories': categories,
        'event_date': event.date,  # Explicitly pass the saved event date
    })

def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('admin_event_control')
    return redirect('admin_event_control')

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            event = form.save(commit=False)
            if 'image' in request.FILES:  # Check if an image is uploaded
                event.image = request.FILES['image']  # Save the uploaded image file
            event.save()  # Save the event instance
            return redirect('admin_event_control')
        else:
            messages.error(request, 'Failed to create event. Please check the form for errors.')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})

@login_required(login_url='login')  # Redirect to login page if not authenticated
def member_dashboard(request):
    events = Event.objects.none()  # Default to no events

    if request.user.is_authenticated and request.user.membership_type:
        if request.user.membership_type.name == "Community Membership":
            events = Event.objects.filter(category="Meetups")
        elif request.user.membership_type.name == "Creative Workspace Membership":
            events = Event.objects.filter(category__in=["Meetups", "Creative Sessions"])
        elif request.user.membership_type.name == "Key Access Membership":
            events = Event.objects.all()
        elif request.user.membership_type.name == "Individual Membership":
            events = Event.objects.none()  # Explicitly show no events

    # Fetch the IDs of events already booked by the user
    user_booked_event_ids = Booking.objects.filter(user=request.user).values_list('event_id', flat=True)
    for event in events:
        # Mark events as booked if the user has already booked them
        event.is_booked = event.id in user_booked_event_ids

    joined_courses = request.user.joined_courses.all()  # Fetch courses joined by the user

    return render(request, "MemberDashboard.html", {
        'events': events,
        'joined_courses': joined_courses,
    })

def membership_dashboard(request):
    base_plan_benefits = MembershipBenefit.objects.filter(plan_type='Base')
    upgraded_plan_benefits = MembershipBenefit.objects.filter(plan_type='Upgraded')
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
            booking.user = request.user  # Assign the logged-in user
            booking.save()
            return redirect('member_dashboard')
    else:
        form = BookingForm()
    return render(request, 'BookEvent.html', {'form': form, 'event': event})

def membership_benefits(request):
    return render(request, 'MembershipBreakdownBenefits.html')

def Register_view(request):
    if request.method == "POST":
        Firstname = request.POST['Firstname']
        Lastname = request.POST['Lastname']
        username = request.POST['username']
        Gender = request.POST['Gender']
        phone_number = request.POST['PhoneNumber']
        email = request.POST['email']
        password = request.POST['password']
        Interests = request.POST['Interests']
        date_of_birth = request.POST['DateOfBirth']
        address = request.POST['Address']

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return render(request, "register.html")

        try:
            # Automatically assign "Individual Membership"
            membership = Membership.objects.get(name="Individual Membership")

            user = CustomUser(
                username=username,
                email=email,
                first_name=Firstname,
                last_name=Lastname,
                phone_number=phone_number,
                gender=Gender,
                interests=Interests,
                date_of_birth=date_of_birth,
                address=address,
                membership_type=membership
            )
            user.set_password(password)  # Hash the password
            user.save()

            register_entry = Register(
                user=user,
                first_name=Firstname,
                last_name=Lastname,
                phone_number=phone_number,
                email=email,
                interests=Interests,
                gender=Gender,
                date_of_birth=date_of_birth,
                address=address,
                membership_type="Individual Membership"  # Save as a string for the Register model
            )
            register_entry.save()

            auth_login(request, user)
            messages.success(request, "Registration successful! You can now log in.")
            return redirect("member")
        except Membership.DoesNotExist:
            messages.error(request, "Default membership type not found. Please contact support.")
            return render(request, "register.html")
        except IntegrityError:
            messages.error(request, "An account with this username or email already exists.")
            return render(request, "register.html")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
            return render(request, "register.html")

    return render(request, "register.html")

@csrf_exempt
def customuser_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        logger.info(f"Attempting login for username: {username}")
        
        user = authenticate(username=username, password=password)
        if user is not None:
            logger.info(f"Authentication successful for username: {username}")
            login(request, user)
            return redirect('MemberDashboard')
        else:
            logger.warning(f"Authentication failed for username: {username}")
            messages.error(request, 'Invalid username or password.')
    return render(request, 'member.html')

@login_required(login_url='login')
def view_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'profile.html', {'user': request.user})

@login_required(login_url='login')
def edit_profile(request):
    custom_user = request.user
    # Ensure the profile exists
    if not hasattr(custom_user, 'profile'):
        Profile.objects.create(user=custom_user)
    profile = custom_user.profile

    if request.method == 'POST':
        custom_user.username = request.POST.get('username', custom_user.username)
        custom_user.first_name = request.POST.get('Firstname', custom_user.first_name)
        custom_user.last_name = request.POST.get('Lastname', custom_user.last_name)
        custom_user.email = request.POST.get('email', custom_user.email)
        custom_user.interests = request.POST.get('Interests', custom_user.interests)
        
        profile.image = request.FILES.get('image', profile.image)  # Update profile picture if provided
        
        custom_user.save()  # Save the updated data
        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('view_profile')
    return render(request, 'editprofile.html', {'user': request.user})

@csrf_exempt
def delete_member(request, member_id):
    if request.method == 'POST':
        try:
            logger.info(f"Attempting to delete member with ID: {member_id}")
            member = get_object_or_404(CustomUser, id=member_id)
            member.delete()
            logger.info(f"Member with ID {member_id} deleted successfully.")
            return JsonResponse({'success': True, 'message': 'Member deleted successfully.'})
        except CustomUser.DoesNotExist:
            logger.error(f"Member with ID {member_id} does not exist.")
            return JsonResponse({'success': False, 'message': 'Member does not exist.'}, status=404)
        except Exception as e:
            logger.error(f"Error deleting member with ID {member_id}: {str(e)}")
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=500)
    logger.warning(f"Invalid request method for deleting member with ID {member_id}")
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

def profile(request):
    return render(request, 'profile.html')

def events_by_category(request):
    events = Event.objects.none()  # Default to no events

    if request.user.is_authenticated and request.user.membership_type:
        if request.user.membership_type.name == "Community Membership":
            events = Event.objects.filter(category="Meetups")
        elif request.user.membership_type.name == "Creative Workspace Membership":
            events = Event.objects.filter(category__in=["Meetups", "Creative Sessions"])
        elif request.user.membership_type.name == "Key Access Membership":
            events = Event.objects.all()
        elif request.user.membership_type.name == "Individual Membership":
            events = Event.objects.none()  # Explicitly show no events

    user_booked_event_ids = Booking.objects.filter(user=request.user).values_list('event_id', flat=True)
    categories = {
        "Meetups": events.filter(category="Meetups"),
        "Creative Sessions": events.filter(category="Creative Sessions"),
        "Workshops": events.filter(category="Workshops"),
    }

    for category, category_events in categories.items():
        for event in category_events:
            event.is_booked = event.id in user_booked_event_ids

    return render(request, "events_by_category.html", {"categories": categories})

from django.views.decorators.http import require_POST

@require_POST
@login_required(login_url='login')
def add_to_user_events(request):
    event_id = request.POST.get('event_id')
    if not event_id:
        return JsonResponse({'success': False, 'message': 'No event ID provided.'}, status=400)

    try:
        event = Event.objects.get(id=event_id)
        if Booking.objects.filter(user=request.user, event=event).exists():
            return JsonResponse({'success': False, 'message': 'Event is already in your events.'})

        Booking.objects.create(
            user=request.user,
            event=event,
            name=request.user.username,
            email=request.user.email,
            phone=request.user.phone_number or ''
        )
        return JsonResponse({'success': True, 'message': 'Event added successfully.'})
    except Event.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Event does not exist.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required(login_url='login')
def my_events(request):
    booked_events = Booking.objects.filter(user=request.user).select_related('event')
    return render(request, 'my_events.html', {'booked_events': booked_events})

from django.shortcuts import get_object_or_404
from .models import Event
from django.db.models import Prefetch

def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    booked_event_ids = Booking.objects.filter(user=request.user).values_list('event_id', flat=True) if request.user.is_authenticated else []
    context = {
        'event': event,
        'booked_event_ids': booked_event_ids,
    }
    return render(request, 'event_details.html', context)

def membership_status(request):
    membership = request.user.membership_type  # Fetch the user's membership type
    membership_details = {
        'type': membership.name if membership else "No Membership",  # Handle cases where no membership is assigned
        'benefits': membership.benefits.all() if membership else []  # Fetch benefits dynamically
    }
    return render(request, 'MembershipStatus.html', {'membership_details': membership_details})

def admin_membershiptypes(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            name = request.POST.get('name')
            price = request.POST.get('price')
            description = request.POST.get('description')
            if name and price and description:
                Membership.objects.create(name=name, price=price, description=description)
                messages.success(request, f"Membership '{name}' added successfully.")
            else:
                messages.error(request, "All fields are required to add a new membership.")
        elif action == 'edit':
            membership_id = request.POST.get('membership_id')
            membership = get_object_or_404(Membership, id=membership_id)
            membership.name = request.POST.get('name', membership.name)
            membership.price = request.POST.get('price', membership.price)
            membership.description = request.POST.get('description', membership.description)
            membership.save()
            messages.success(request, f"Membership '{membership.name}' updated successfully.")
        elif action == 'delete':
            membership_id = request.POST.get('membership_id')
            membership = get_object_or_404(Membership, id=membership_id)
            membership.delete()
            messages.success(request, f"Membership '{membership.name}' deleted successfully.")

        return redirect('admin_membershiptypes')

    memberships = Membership.objects.all()
    return render(request, 'admin_membershiptypes.html', {'memberships': memberships})

def add_membership(request):
    if request.method == 'POST':
        form = MembershipForm(request.POST)
        if form.is_valid():
            membership = form.save(commit=False)
            membership.save()
            form.save_m2m()  # Save the many-to-many relationship for benefits
            messages.success(request, 'Membership added successfully.')
            return redirect('admin_membershiptypes')
    else:
        form = MembershipForm()
    return render(request, 'add_membership.html', {'form': form})

def manage_membership_benefits(request, membership_id):
    membership = get_object_or_404(Membership, id=membership_id)
    all_benefits = MembershipBenefit.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        benefit_id = request.POST.get('benefit_id')

        if action == 'add' and benefit_id:
            benefit = get_object_or_404(MembershipBenefit, id=benefit_id)
            membership.benefits.add(benefit)
            messages.success(request, f'Benefit "{benefit.name}" added to "{membership.name}".')
        elif action == 'remove' and benefit_id:
            benefit = get_object_or_404(MembershipBenefit, id=benefit_id)
            membership.benefits.remove(benefit)
            messages.success(request, f'Benefit "{benefit.name}" removed from "{membership.name}".')

        return redirect('manage_membership_benefits', membership_id=membership.id)

    return render(request, 'manage_membership_benefits.html', {
        'membership': membership,
        'all_benefits': all_benefits,
    })

def manage_all_benefits(request):
    benefits = MembershipBenefit.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        benefit_id = request.POST.get('benefit_id')

        if action == 'delete' and benefit_id:
            benefit = get_object_or_404(MembershipBenefit, id=benefit_id)
            benefit.delete()
            messages.success(request, f'Benefit "{benefit.name}" deleted successfully.')
        elif action == 'add':
            name = request.POST.get('name')
            description = request.POST.get('description')
            if name:
                MembershipBenefit.objects.create(name=name, description=description)
                messages.success(request, f'Benefit "{name}" added successfully.')
            else:
                messages.error(request, 'Benefit name is required.')

        return redirect('manage_all_benefits')

    return render(request, 'manage_all_benefits.html', {'benefits': benefits})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import MembershipUpgradeRequest, CustomUser, Membership  # Corrected import

@login_required
def request_upgrade(request):
    if request.method == "POST":
        membership_id = request.POST.get("membershipType")
        requested_membership = get_object_or_404(Membership, id=membership_id)  # Fetch the Membership instance
        MembershipUpgradeRequest.objects.create(user=request.user, requested_type=requested_membership)
        messages.success(request, "Your upgrade request has been sent and is awaiting admin approval.")
    memberships = Membership.objects.all()  # Fetch all memberships dynamically
    return render(request, "request_upgrade.html", {"memberships": memberships})

@login_required
def approve_upgrade(request, request_id):
    upgrade_request = get_object_or_404(MembershipUpgradeRequest, id=request_id)
    upgrade_request.user.membership_type = upgrade_request.requested_type  # Assign the Membership instance
    upgrade_request.user.save()
    upgrade_request.is_verified = True
    upgrade_request.save()
    messages.success(request, f"Membership upgrade for {upgrade_request.user.get_full_name()} approved.")
    return redirect('admin_control_membership')

@login_required
def deny_upgrade(request, request_id):
    upgrade_request = get_object_or_404(MembershipUpgradeRequest, id=request_id)
    upgrade_request.is_verified = True
    upgrade_request.save()
    messages.info(request, f"Membership upgrade for {upgrade_request.user.get_full_name()} denied.")
    return redirect('admin_control_membership')

def manage_courses(request):
    courses = Course.objects.all()
    categories = Course.objects.values_list('category__name', flat=True).distinct()

    # Get filter values from the request
    selected_category = request.GET.get('category', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    # Apply filters if provided
    if selected_category:
        courses = courses.filter(category__name=selected_category)
    if start_date:
        courses = courses.filter(date__gte=start_date)
    if end_date:
        courses = courses.filter(date__lte=end_date)

    context = {
        'categories': categories,
        'selected_category': selected_category,
        'start_date': start_date,
        'end_date': end_date,
        'courses': courses,
    }
    return render(request, 'manage_courses.html', context)

def create_course(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_name = request.POST.get('category')
        date = request.POST.get('date')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        logger.debug(f"Creating course with data: name={name}, category={category_name}, date={date}, description={description}, image={image}")

        # Fetch or create the Category instance
        category, created = Category.objects.get_or_create(name=category_name)

        # Save the course
        Course.objects.create(
            name=name,
            category=category,
            date=date,
            description=description,
            image=image
        )

        messages.success(request, "Course created successfully.")
        return redirect('admin_course_control')

    # Render the course creation page if not POST
    return render(request, 'create_course.html')

def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully.')
            return redirect('admin_course_control')
        else:
            messages.error(request, 'Failed to update course. Please check the form for errors.')
    else:
        form = CourseForm(instance=course)
    return render(request, 'edit_course.html', {'form': form, 'course': course})

def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully.')
        return redirect('admin_course_control')
    return HttpResponse(status=405)  # Method not allowed

def course_modules(request):
    courses = Course.objects.none()  # Default to no courses

    if request.user.is_authenticated and request.user.membership_type:
        if request.user.membership_type.name == "Community Membership":
            courses = Course.objects.filter(category__name="Programming")
        elif request.user.membership_type.name == "Creative Workspace Membership":
            courses = Course.objects.filter(category__name__in=["Programming", "Design"])
        elif request.user.membership_type.name == "Key Access Membership":
            courses = Course.objects.filter(category__name__in=["Programming", "Design", "Marketing"])
        elif request.user.membership_type.name == "Individual Membership":
            courses = Course.objects.none()  # Explicitly show no courses

    categories = Category.objects.all()
    selected_category = request.GET.get('category')

    if selected_category:
        courses = courses.filter(category__id=selected_category)

    return render(request, 'CourseModules.html', {
        'courses': courses,
        'categories': categories,
        'selected_category': selected_category,
    })

def join_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.joined_users.add(request.user)  # Add the logged-in user directly
        messages.success(request, f"You have successfully joined the course: {course.name}.")
        return redirect('course_modules')
    return HttpResponse(status=405)  # Method not allowed

from .models import Membership

def request_upgrade_view(request):
    memberships = Membership.objects.all()  # Fetch all memberships
    return render(request, 'request_upgrade.html', {'memberships': memberships})

from django.http import JsonResponse

def get_course_details(request):
    course_id = request.GET.get('course_id')
    try:
        course = Course.objects.get(id=course_id)
        return JsonResponse({
            'name': course.name,
            'date': course.date.strftime('%Y-%m-%d'),
            'description': course.description,
        })
    except Course.DoesNotExist:
        return JsonResponse({'error': 'Course not found'}, status=404)
