from django.contrib import admin
from django.db.models import Q
from django.contrib import admin
import stripe.error
from .models import CartItem,Order,OrderItem
import logging
from django.conf import settings
from django.contrib import admin
import stripe
from .admins import OrderAdmin,OrderItemAdmin
stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger('ecommerce')

admin.site.register(CartItem)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(Order,OrderAdmin)



