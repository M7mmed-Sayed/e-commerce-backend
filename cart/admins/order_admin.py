from django.contrib import admin

from django.contrib import admin
import stripe.error
import logging
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.contrib import admin, messages
from ..models import Order,OrderStatus
import stripe
from accounts.models import UserType
stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger('ecommerce')

class OrderAdmin(admin.ModelAdmin):
    actions = ("refund", )
    list_display = ["user", "created_at", "order_status","payment_id"]
    list_filter=['order_status',]
    @admin.action(description='refund the selected orders')
    def refund(self, request, queryset):
        if request.user.usertype not in[ UserType.ADMIN]:
            messages.success(request, "only admins can refund the order payments")
            raise PermissionDenied("u don'y have access to this action")
            
        for obj in queryset:
            try:

                refund =stripe.Refund.create(payment_intent=obj.payment_id)
                if refund.status=="succeeded":
                    obj.order_status=OrderStatus.REFUND
                    obj.save()
                    logger.info(f' Successful refund object id: {obj.id} payment intent:{obj.payment_id} ')
                    messages.success(request, f'Successful refund object id: {obj.id} payment intent:{obj.payment_id}  ')
                else:
                    logger.error(f'Un Successful refund object id: {obj.id} payment intent:{obj.payment_id} ')
                    
            except Exception as e:
                logger.warning(f'Un Successful refund object id: {obj.id} payment intent:{obj.payment_id}  {e}')
                messages.warning(request, f'Un Successful refund object id: {obj.id} payment intent:{obj.payment_id} Exception {e} ')
       


