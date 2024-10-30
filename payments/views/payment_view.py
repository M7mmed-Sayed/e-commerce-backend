import json

import stripe
import stripe.error
from django.conf import settings
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import CartItem, OrderItem, Order, OrderStatus
from cart.serializers import OrderSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY
SUCCESS_URL=settings.SUCCESS_URL
CANCEL_URL=settings.CANCEL_URL

class StripeCheckoutView(CreateAPIView):
    serializer_class = OrderSerializer

    def post(self, request):
        with transaction.atomic():
            try:
                user = request.user
                # get the  cart /items for the current user
                cart_items = CartItem.objects.filter(user=user)
                # if there is no items so we cann't do an order
                # useing transaction to validate that

                order_data = {
                    'shipping_address': 'new Cairo',
                    'shipping_cost': '5',
                    'order_status': OrderStatus.NONE
                }
                order_serializer = self.get_serializer(data=order_data)
                if order_serializer.is_valid():
                    order = order_serializer.save(user=user, shipping_cost=5, order_status=OrderStatus.NONE)
                    for cart_item in cart_items:
                        product = cart_item.product
                        OrderItem.objects.create(
                            order=order,
                            user=user,
                            product=product,
                            quantity=cart_item.quantity,
                            order_item_price=product.price
                        )
                    # cart_items.delete()
                    total = int(sum(item.product.price * item.quantity * 10 for item in cart_items))
                    # useing transaction to validate that
                    line_items = []
                    shipping_cost = 20
                    # items to ui
                    for item in cart_items:
                        line_items.append({
                            'price_data': {
                                'currency': 'usd',
                                'product_data': {
                                    'name': item.product.name,
                                },
                                'unit_amount': int(item.product.price * 100),  # convert to sent
                            },
                            'quantity': item.quantity,
                        })
                    # shipping cost as cost
                    line_items.append({
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'Shipping Cost',
                            },
                            'unit_amount': shipping_cost,
                        },
                        'quantity': 1,

                    })

                    checkout_session = stripe.checkout.Session.create(
                        # payment_method=payment_method.id,
                        payment_method_types=['card'],
                        line_items=line_items,
                        mode='payment',
                        success_url=SUCCESS_URL,
                        cancel_url=CANCEL_URL ,
                        payment_intent_data={
                            'metadata': {
                                'order_id': order.id
                            },
                        },
      
                    )
                    print(checkout_session.url)
                    return Response({"payment-url": checkout_session.url}, status=status.HTTP_200_OK)
            except  Exception as e:
                print(e)
                transaction.set_rollback(True)
                return Response({"message": 'no'}, status=status.HTTP_400_BAD_REQUEST)



class StripePeymentView(CreateAPIView):
    def post(self, request):
        try:

            user = request.user
            # get the  cart /items for the current user
            cart_items = CartItem.objects.filter(user=user)
            # if there is no items so we cann't do an order
            if not cart_items.exists():
                return Response({'no items': 'the cart is Empty'}, status=status.HTTP_400_BAD_REQUEST)
            for cart_item in cart_items:
                product = cart_item.product
                if product.stock_quantity < cart_item.quantity:
                    return Response({'Product': f"Not enough  product at {product.name} stock_quantity."},
                                    status=status.HTTP_400_BAD_REQUEST)
            total = int(sum(item.product.price * item.quantity * 10 for item in cart_items))
            # using transaction to validate that
            line_items = []

            shipping_cost = 200
            # items to ui
            for item in cart_items:
                product_stripe = stripe.Product.create(name=item.product.name)
                price_stripe = stripe.Price.create(
                    product=product_stripe.id,
                    unit_amount=int(item.product.price * 100),
                    currency="usd",
                )
                line_items.append({'price': price_stripe.id, 'quantity': item.quantity})
            # shipping cost as cost
            payment_methods = ['card', 'link', ]
            checkout_session = stripe.PaymentLink.create(

                line_items=line_items,
                restrictions={"completed_sessions": {"limit": 1}},
                payment_method_types=payment_methods,
                currency='usd',
                custom_fields=[
                    {
                        "key": "engraving",
                        "label": {"type": "custom", "custom": "Personalized engraving"},
                        "type": "text",
                    }, ],
                after_completion={"type": "redirect", "redirect": {"url": "http://127.0.0.1:8000//cart/checkout/"}},
            )
            print(checkout_session.id)
            print(checkout_session.url)
            return Response({"message": checkout_session.url}, status=status.HTTP_200_OK)
        except  Exception as e:
            print(e)
            return Response({"message": 'no'}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body.decode('utf-8')
    event = json.loads(payload)

    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        print(payment_intent.get('metadata', {}))
        order_id = payment_intent.get('metadata', {}).get('order_id')
        print("secucces")
        print("joind")
        print(order_id)
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                order.order_status = OrderStatus.PROCESSING
                order.payment_id = payment_intent['id']
                order.save()
                print(order)
                return JsonResponse({'status': 'success', 'message': 'Order updated successfully'}, status=200)
            except Order.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Order not found'}, status=404)

    # Handle other event types or errors
    return JsonResponse({'status': 'error', 'message': 'Unhandled event type'}, status=400)
