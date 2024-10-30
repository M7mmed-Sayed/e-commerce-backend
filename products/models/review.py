from django.db import models
from accounts.models import AppUser
from ..models import Product
class Review(models.Model):
    customer = models.ForeignKey(AppUser, on_delete=models.SET_NULL,null=True)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): 
        return f'{self.customer.username} add review {self.comment}  rating {self.rating}'
    