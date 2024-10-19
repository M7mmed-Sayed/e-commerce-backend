from django.contrib import admin
import re
import csv
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import admin
import stripe.error
import logging
from django.conf import settings
from django.contrib import admin, messages
import stripe
from ..models import OrderItem
stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger('ecommerce')


class OrderItemAdmin(admin.ModelAdmin):
    actions = ("export_as_csv", )

    list_display = ["user","order", "product", "quantity","order_item_price",'orignal_price',"created_at",'order_status',]

    search_fields = ["user__username","product__name__icontains"]
    
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        regex = '(19|20)\d\d-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])'
        try:
            date_search = re.fullmatch(regex, search_term)
            if date_search is not None:
                queryset=self.model.objects.filter(Q(order__created_at__gt=search_term))
        except Exception as e:
            pass
        return super().get_search_results(request, queryset, '')

    @admin.action(description='export the selected items')
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        writer = csv.writer(response)
        field_names = self.list_display
        writer.writerow(field_names) 
        for obj in queryset:
            row = []
            for field in field_names:
                row.append(getattr(obj, field))
            writer.writerow(row) 
        messages.success(request, "Successfully saved!")
        return response

