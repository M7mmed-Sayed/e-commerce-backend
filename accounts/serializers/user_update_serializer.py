
import re

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from ..models import AppUser
from .dynamic_serializer import DynamicFieldsModelSerializer
class UserUpdateSerializer(DynamicFieldsModelSerializer):
    username = serializers.CharField(read_only=True)
    class Meta:
        model = AppUser
        fields = (
             'username', 'first_name', 'last_name','phone_number', 'city')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone_number': {'required': True}
        }

    def validate_phone_number(self, value):
        regex = '([+]?01[0125]\d{8})'
        phone = re.fullmatch(regex, value)
        if phone is None:
            raise serializers.ValidationError(
                {"phone": "Incorrect phone Number format 11 digits,it must start with 010,011,012, or 015."})
        return value
   
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.city = validated_data.get('city', instance.city)
        instance.save()

        return instance
    
