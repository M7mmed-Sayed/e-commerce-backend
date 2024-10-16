from django.db import models
from accounts.models import AppUser
from products.models import Product
class OrderStatus(models.TextChoices):
    PROCESSING = "PROCESSING", "Processing"
    SHIPPED = "SHIPPED", "Shipped"
    DELIVERED = "DELIVERED", "Delivered"

class Order(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.SET_NULL,null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=15, choices=OrderStatus.choices, default=OrderStatus.PROCESSING)
    shipping_address = models.CharField(max_length=255)
    shipping_cost = models.DecimalField(max_digits=7, decimal_places=2,null=True)
    def __str__(self):
        return f'{self.shipping_address} -- {self.shipping_cost} -- {self.user}'

   
    