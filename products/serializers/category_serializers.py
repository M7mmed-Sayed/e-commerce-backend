
import re

from rest_framework import serializers
from ..models import Category
class CategorySerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Category
        fields = ('id','name','description' )
        extra_kwargs = {
            'name': {'required': True},
        }
    