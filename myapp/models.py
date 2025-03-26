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

class MembershipBenefit(models.Model):
    name = models.CharField(max_length=200)  # Name of the benefit
    description = models.TextField()  # Description of the benefit
    utilized = models.BooleanField(default=False)  # Whether the benefit has been utilized

    def __str__(self):
        return self.name

class Booking(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='bookings')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name} - {self.event.name}"
