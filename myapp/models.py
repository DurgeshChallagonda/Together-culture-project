from django.db import models  # type: ignore


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