

from rest_framework import serializers
from ..models import Product
class ProductSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    num_reviews = serializers.IntegerField(read_only=True)# it will update by 1 after user add comments
    rating = serializers.IntegerField(read_only=True)# it will update by value fo user review rating and product over rating will be rating/num_reviews
    id = serializers.IntegerField(read_only=True)
    seller=serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "category",
            "description",
            "image",
            "price",
            'stock_quantity',
            'rating',
            'num_reviews',
            'created_at',
            'seller',
        )
        lookup_field = "id"