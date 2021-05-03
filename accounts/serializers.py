from rest_framework import serializers
from .models import CustomUser
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer) :

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'phone', 'bank_account'] 
