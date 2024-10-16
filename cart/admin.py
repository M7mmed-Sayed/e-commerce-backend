from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CartItem,OrderItem,Order

# Register your models here.
admin.site.register(Order)

admin.site.register(CartItem)
admin.site.register(OrderItem)
