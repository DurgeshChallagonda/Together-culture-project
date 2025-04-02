<<<<<<< Updated upstream
from django.contrib import admin  # type: ignore
from .models import User, Member
# Register your models here.

admin.site.register(User)
=======
from django.contrib import admin
from .models import CustomUser
from .models import Member

# Register your models here.
admin.site.register(CustomUser)
>>>>>>> Stashed changes
admin.site.register(Member)
