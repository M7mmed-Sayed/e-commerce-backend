from django.core.management  import BaseCommand
from time import sleep
from datetime import datetime
from cart.models import OrderStatus,Order
from django.db.models import Q

class Command(BaseCommand):
    help="print hello"
    def handle(self, *args, **options):
        print(" in command done yes ")
        query=Order.objects.filter(Q(order_status=OrderStatus.NONE)|Q(order_status__isnull=True))
        print(query)
        cur= datetime.now()
        query.delete()
        self.stdout.write(f"the current time is {cur}")
        sleep(10)