<<<<<<< Updated upstream
from rest_framework import serializers # type: ignore
from .models import Member

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'
=======
from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'interests', 'gender', 'date_of_birth', 'address', 'membership_type']
>>>>>>> Stashed changes
