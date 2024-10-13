from rest_framework import serializers
from ..models import OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    """
    using it to list order items at order serializers
    """
    product_name = serializers.ReadOnlyField(source='product.name') # get the name to list at the view
    class Meta:
        model = OrderItem
        fields = ( 'product', 'quantity','product_name', 'order_item_price')
