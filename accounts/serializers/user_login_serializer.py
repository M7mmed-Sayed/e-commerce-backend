
from django.contrib.auth import authenticate

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from ..models import AppUser
class UserLoginSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255,read_only=True)
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    username = serializers.CharField(max_length=30, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        login_user = authenticate(email=email, password=password)
        if login_user is None:
            raise serializers.ValidationError(
               {'error': 'Invalid credentials Invalid Email or Password',}
               
            )
        token, _ = Token.objects.get_or_create(user=login_user)
        user = AppUser.objects.get(email=email)
        response_data={
            'id':user.id,
            'email':user.email,
            'username':user.username,
            'token': token.key
            }
        return response_data

