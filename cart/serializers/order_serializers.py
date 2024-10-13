

from rest_framework import serializers
from ..models import Order
from .order_item_serializers import OrderItemSerializer
from accounts.serializers.dynamic_serializer import DynamicFieldsModelSerializer
class OrderSerializer(DynamicFieldsModelSerializer):
    id = serializers.IntegerField(read_only=True)
    shipping_cost = serializers.DecimalField(read_only=True,max_digits=8,decimal_places=2)
    full_name = serializers.SerializerMethodField()
    items = OrderItemSerializer(many=True, read_only=True)# to get the items for the orders
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = (
            "id",
            'full_name',
            "shipping_cost",
            "shipping_address",
            "order_status",
            "total_price",
            'created_at',
            'items'
        )
        lookup_field = "id"
    # read only field method to get the user full name
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    # get total price for each itme X it's quantity
    def get_total_price(self, obj):
        total = sum(item.order_item_price * item.quantity for item in obj.items.all())
        return total
    