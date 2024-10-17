from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView,RetrieveAPIView,UpdateAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from ..models import OrderStatus,Order,CartItem,OrderItem
from rest_framework import status
from products.models import Product
from ..serializers import OrderSerializer
from django.db import transaction
from accounts.models import UserType
import stripe

class CheckOutOrderView(CreateAPIView):
    """
        check out cart items to be ordered to the user
        using transaction to validate that
        we created an order
        check if all products have the enough stock_quantity
        create a list of orders items from  the cart items and link it with the order
        remove the cart items after create the order
        
        """
    serializer_class = OrderSerializer
    permission_classes=[IsAuthenticated]
    def create(self, request, *args, **kwargs):
        user = request.user
        # get the  cart /items for the current user
        cart_items = CartItem.objects.filter(user=user)
        # if there is no items so we cann't do an order
        if not cart_items.exists():
            return Response({'no': 'the cart is Empty'}, status=status.HTTP_400_BAD_REQUEST)
        checkout_id = request.GET.get('session_id', None)
        """
        refund the payment
        roalback=stripe.checkout.Session.retrieve(checkout_id)
        print(f"id : {roalback.payment_intent}")
        refund =stripe.Refund.create(payment_intent=roalback.payment_intent)
        print(refund)
        """
        #useing transaction to validate that
        with transaction.atomic():
            order_data = {
                'shipping_address': request.data.get('shipping_address'),
                'shipping_cost': '5',
                'order_status':OrderStatus.PROCESSING
            }
            order_serializer = self.get_serializer(data=order_data)
            if order_serializer.is_valid():
                order = order_serializer.save(user=user,shipping_cost=5)
                for cart_item in cart_items:
                    product = cart_item.product
                    if product.stock_quantity < cart_item.quantity:
                        return Response({'Product': f"Not enough  product at {product.name} stock_quantity."}, status=status.HTTP_400_BAD_REQUEST)
                    #product.stock_quantity -= cart_item.quantity
                    product.save()
                    OrderItem.objects.create(
                        order=order,
                        user=user,
                        product=product,
                        quantity=cart_item.quantity,
                        order_item_price=product.price 
                    )
                respone={
                    'respone':
                    order_serializer.data,
                    'checkout_id':checkout_id
                }

                #cart_items.delete()
                return Response(respone, status=status.HTTP_201_CREATED)
            else:
                #rollback if the is at least one error or missing something
                transaction.set_rollback(True)
                return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   

class OrderViewSet(ModelViewSet):
    """
    to get one or list of orders 
    update the order_status with desierd status
    """
    serializer_class = OrderSerializer
    permission_classes=[IsAuthenticated]
    queryset=Order.objects.all()
    # if user is not have administrator action list only his orders
    def get_queryset(self):
        user=self.request.user
        query_set=Order.objects.filter(user=user)
        if self.request.user.usertype not in[ UserType.ADMIN,UserType.EMPLOYEE]:
            query_set=Order.objects.filter(user=user)
        return query_set


    # only owner can retrive his orders or the admin users
    def retrieve(self, request, *args, **kwargs):
        if request.user!= self.get_object().user and request.user.usertype not in[ UserType.ADMIN,UserType.EMPLOYEE] :
                 return Response({"Unauthorized": "only owner order or admin can  see"},status=status.HTTP_401_UNAUTHORIZED)
        return super().retrieve(request, *args, **kwargs)

        
    # only admin can edit the order & edit only order_status fields
    def update(self, request, *args, **kwargs):
        if  request.user.usertype not in[ UserType.ADMIN,UserType.EMPLOYEE] :
                return Response({"Unauthorized": "only  admin can  Edit"},status=status.HTTP_401_UNAUTHORIZED)
        order_status=request.data.get("order_status")
        try:
            order=self.get_object()
            serializer=self.get_serializer(order,data={'order_status':order_status},partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CartItem.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    
    
