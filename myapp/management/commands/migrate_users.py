from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import CustomUser

class Command(BaseCommand):
    help = 'Migrate users from the default User model to the CustomUser model'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            if not CustomUser.objects.filter(username=user.username).exists():
                CustomUser.objects.create(
                    username=user.username,
                    email=user.email,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    is_staff=user.is_staff,
                    is_active=user.is_active,
                    is_superuser=user.is_superuser,
                    date_joined=user.date_joined,
                    membership_type='Individual Membership'  # Default membership type
                )
        self.stdout.write(self.style.SUCCESS('Successfully migrated users to CustomUser model.'))
