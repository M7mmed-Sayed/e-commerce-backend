import time
from celery import shared_task
from ecommerce.celery import app
from cart.models import OrderStatus,Order,OrderItem
import logging
from datetime import datetime,timedelta
from django.db.models import Q
from django.db import transaction
from products.models import Product
logger = logging.getLogger('ecommerce')

@shared_task()
def testing_celery():
   for x in range(10):
        print(x)
        logger.debug(x)
        time.sleep(1)

@app.task
def testing_schedule_celery():
    cur_date=datetime.now()
    logger.debug(f"celery-testing-task {datetime.now()}  sub {cur_date+timedelta(hours=-4)} ")



@app.task
def delete_non_complated_orders():
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



@app.task
def shippping_orders():
    cur_date=datetime.now()+timedelta(days=-17)
    orders=Order.objects.filter((Q(order_status=OrderStatus.PROCESSING))&Q(created_at__lte=cur_date))
    for order in orders:
        order.order_status=OrderStatus.SHIPPED
        order.save()
    #orders.delete()
    logger.debug(f"celery-shippping_orders-task {cur_date} qr{orders}")













   

