
from django.contrib.auth import authenticate
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from ..tasks import testing_celery
from cart.models import OrderStatus,Order,OrderItem
from products.models import Product
from django.db import transaction
from django.db.models import Q
from datetime import datetime,timedelta


import logging
logger = logging.getLogger('ecommerce')
@api_view(['POST'])
def test_celery_view(request):
    #testing_celery.delay()
    cur_date=datetime.now()+timedelta(days=-15)
    orders=Order.objects.filter((Q(order_status=OrderStatus.NONE)|Q(payment_id__isnull=True))&Q(created_at__lte=cur_date))
    for order in orders:
        with transaction.atomic():
            try:
                items=OrderItem.objects.filter(order=order)
                for item in items:
                    try:
                        product = Product.objects.select_for_update().get(pk=item.product.id)
                        updated_quantity = product.stock_quantity+item.quantity
                        product.stock_quantity=updated_quantity
                        product.save()
                        item.delete()
                    except Product.DoesNotExist:
                        raise
                logger.debug(f"{order.id} {items}  was deleted after expierd with scheduling task")
                items.delete()
                order.delete()
            except:
                transaction.set_rollback(True)
                
                    
                    
                


        #orders.delete()
    return Response({"message": "ok"}, status=status.HTTP_200_OK)


