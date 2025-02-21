from rest_framework import serializers # type: ignore
from .models import Member

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'