from django.contrib import admin  # type: ignore
from .models import User, Member
# Register your models here.

admin.site.register(User)
admin.site.register(Member)
