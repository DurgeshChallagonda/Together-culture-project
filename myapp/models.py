from django.db import models  # type: ignore
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    MEMBERSHIP_CHOICES = [
        ('Individual Membership', 'Individual Membership'),
        ('Community Membership', 'Community Membership'),
        ('Workspace Membership', 'Workspace Membership'),
        ('Organisational Membership', 'Organisational Membership'),
    ]
    membership_type = models.CharField(
        max_length=50,
        choices=MEMBERSHIP_CHOICES,
        default='Individual Membership'
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Add phone number
    interests = models.TextField(blank=True, null=True)  # Add interests
    gender = models.CharField(max_length=10, blank=True, null=True)  # Add gender
    date_of_birth = models.DateField(blank=True, null=True)  # Add date of birth
    address = models.TextField(blank=True, null=True)  # Add address

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

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.username} - {self.password}"
    
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