from django.db import models
from accounts.models import AppUser
from products.models import Product
from ..models import Order

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    user = models.ForeignKey(AppUser, on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=1)
    order_item_price = models.DecimalField(max_digits=8, decimal_places=2)  # the cost for the product is not static so maybe the product price up/dwon , when i wanna to list the items it's giving me the cost of item at the order not the current product pricr
    def __str__(self):
        return f'{self.quantity} -- {self.product} -- {self.order_item_price}'