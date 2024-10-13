from django.db import models
from accounts.models import AppUser
from products.models import Product
class CartItem(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.SET_NULL,null=True)  
    product=models.ForeignKey(Product, on_delete=models.SET_NULL,null=True) 
    quantity = models.IntegerField(default=1,null=False) 
    class Meta:
        constraints=[models.UniqueConstraint(fields=['user','product'],name="unique_cart_user_product")]
    