from rest_framework import serializers

from ..models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'product', 'comment','rating', 'created_at']
        read_only_fields = ['customer', 'created_at', 'product']
    
