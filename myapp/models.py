<<<<<<< Updated upstream
from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, choices=[
        ('Workshops', 'Workshops'),
        ('Meetups', 'Meetups'),
        ('Creative Sessions', 'Creative Sessions'),
    ])
    description = models.TextField()

    def __str__(self):
        return self.name
=======
from django.db import models, IntegrityError  # Import IntegrityError
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings  # Import settings to reference the custom user model
from django.core.exceptions import ValidationError  # Import ValidationError

class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    username = models.CharField(max_length=150, unique=True)  # Ensure this field is unique
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
        null=True
    )
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    membership_type = models.ForeignKey(
        'Membership',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    interests = models.TextField(blank=True, null=True)
    events = models.ManyToManyField('Event', related_name='users', blank=True)
    booked_events = models.ManyToManyField('Event', through='Booking', related_name='booked_users', blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # Avoid conflict with auth.User.groups
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",  # Avoid conflict with auth.User.user_permissions
        blank=True
    )
>>>>>>> Stashed changes

    def save(self, *args, **kwargs):
        if not self.pk and not self.password.startswith('pbkdf2_'):  # Ensure password is hashed
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.username} - {self.password}"
<<<<<<< Updated upstream

class Member(models.Model):
    Firstname = models.CharField(max_length=50)
    Lastname = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    Dateofbirth = models.DateField()
    Gender = models.CharField(max_length=50)
    MobileNumber = models.IntegerField()
    Address = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    confirm_password = models.CharField(max_length=50)
    Interests = models.CharField(max_length=50)
    
    def __str__(self):
        return self.username

=======
    
class Event(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()  # Ensure this is a DateField or DateTimeField
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    bookings = models.ManyToManyField('CustomUser', through='Booking', related_name='event_bookings')

    def __str__(self):
        return self.name
    
>>>>>>> Stashed changes
class MembershipBenefit(models.Model):
    name = models.CharField(max_length=200)  # Name of the benefit
    description = models.TextField()  # Description of the benefit
    utilized = models.BooleanField(default=False)  # Whether the benefit has been utilized

    def __str__(self):
        return self.name

class Booking(models.Model):
<<<<<<< Updated upstream
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='bookings')
=======
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='event_bookings')  # Adjust related_name
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_bookings', default=1)  # Add default value
>>>>>>> Stashed changes
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name} - {self.event.name}"
<<<<<<< Updated upstream
=======
    
class Register(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # Ensure CASCADE is used
    first_name = models.CharField(max_length=50)  # Updated field name
    last_name = models.CharField(max_length=50)  # Updated field name
    phone_number = models.CharField(max_length=15)  # Renamed from mobile_number
    email = models.EmailField()
    interests = models.CharField(max_length=255)  # Updated field name
    gender = models.CharField(max_length=10)  # Updated field name
    membership_type = models.CharField(  # Removed 'choices' argument
        max_length=50,
        default='Individual Membership'  # Ensure default is set
    )
    date_of_birth = models.DateField(blank=True, null=True)  # Added field
    address = models.TextField(blank=True, null=True)  # Added field

    def clean(self):
        """Validate membership_type against available Membership names."""
        valid_memberships = Membership.objects.values_list('name', flat=True)
        if self.membership_type not in valid_memberships:
            raise ValidationError(f"Invalid membership type: {self.membership_type}")

    def __str__(self):
        return self.user.username

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Ensure CASCADE is used
    image = models.ImageField(default='/media/default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

class Member(models.Model):
    custom_user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        default=1  # Provide a one-off default value (e.g., the ID of an existing user)
    )
    username = models.CharField(max_length=150, unique=True, default="DefaultUsername")  # Provide a default value
    email = models.EmailField(unique=True, default="default@example.com")  # Provide a default value
    first_name = models.CharField(max_length=30, default="DefaultFirstName")  # Provide a default value
    last_name = models.CharField(max_length=30, default="DefaultLastName")  # Provide a default value
    date_joined = models.DateTimeField(auto_now_add=True)  # Use only auto_now_add

    def __str__(self):
        return self.username

class Membership(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Allow dynamic membership types
    price = models.CharField(max_length=20, blank=True, null=True)  # Optional price
    description = models.TextField(blank=True, null=True)  # Optional description
    benefits = models.ManyToManyField('MembershipBenefit', related_name='memberships', blank=True)

    def __str__(self):
        return self.name

    @staticmethod
    def sync_with_membership_choices():
        """Sync Membership model with CustomUser.MEMBERSHIP_CHOICES."""
        existing_memberships = set(Membership.objects.values_list('name', flat=True))
        for choice, _ in CustomUser.MEMBERSHIP_CHOICES:
            if choice not in existing_memberships:
                Membership.objects.create(name=choice)

    @staticmethod
    def ensure_default_membership():
        """Ensure 'Individual Membership' exists as a default membership."""
        if not Membership.objects.filter(name="Individual Membership").exists():
            Membership.objects.create(name="Individual Membership", price="0", description="Default individual membership.")

# Ensure this method is called during app initialization
from django.apps import AppConfig

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        from .models import Membership
        Membership.sync_with_membership_choices()
        Membership.ensure_default_membership()

@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class MembershipUpgradeRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use the custom user model
    requested_type = models.ForeignKey('Membership', on_delete=models.CASCADE)  # Link to Membership model
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.requested_type.name}"

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField()
    image = models.ImageField(upload_to='media/course_images/', blank=True, null=True)
    joined_users = models.ManyToManyField(
        'CustomUser',  # Use the CustomUser model
        related_name='joined_courses',
        blank=True
    )

    def __str__(self):
        return self.name

    def clean(self):
        if not Category.objects.filter(id=self.category_id).exists():
            raise ValidationError(f"Category with ID {self.category_id} does not exist.")
>>>>>>> Stashed changes
