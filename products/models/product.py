from django.db import models
from accounts.models import AppUser
from ..models import Category
class Product(models.Model):
    seller = models.ForeignKey(AppUser, on_delete=models.SET_NULL,null=True)  
    category = models.ManyToManyField(Category, blank=False)
    name = models.CharField(max_length=80)
    description = models.TextField(max_length=200, default="Empty description.")
    image = models.ImageField(upload_to="products/images", null=True, blank=True)
    price = models.DecimalField(max_digits=15,decimal_places=2, default=0.0)
    stock_quantity = models.IntegerField(default=1) 
    rating = models.IntegerField(default=0)
    num_reviews = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return self.name
    class Meta:
        indexes =[models.Index(fields=['name'])]