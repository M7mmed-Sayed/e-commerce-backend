

from rest_framework import serializers
from ..models import CartItem
class CartItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user=serializers.PrimaryKeyRelatedField(read_only=True)
    product=serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = CartItem
        fields = (
            "id",
            "user",
            "product",
            'quantity',
        )
        lookup_field = "id"
    def validate_quantity(self, value):
        if value<1:
            raise serializers.ValidationError("quantity must be postitive integer")
        return value
    