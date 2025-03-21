from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone

class CustomUser(AbstractUser):
    MEMBERSHIP_CHOICES = [
        ('Individual Membership', 'Individual Membership'),
        ('Community Membership', 'Community Membership'),
        ('Workspace Membership', 'Workspace Membership'),
        ('Organisational Membership', 'Organisational Membership'),
    ]
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    membership_type = models.CharField(
        max_length=50,
        choices=MEMBERSHIP_CHOICES,
        default='Individual Membership'
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
        null=True
    )
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

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