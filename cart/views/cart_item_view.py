from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView,RetrieveAPIView,UpdateAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from ..models import CartItem
from rest_framework import status
from products.models import Product
from ..serializers import CartItemSerializer
from accounts.models import UserType
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.decorators import api_view,permission_classes
from django.db import transaction
from celery import shared_task
from time import sleep
from cart.models import OrderStatus,Order
import logging
logger = logging.getLogger('ecommerce')


class CartItemViewSet(ModelViewSet):
    """
    view for add to cart products
    user can add to cart with product id  and set quantity by 1
    user can edit  product at the cart with the id 
       - if the quantity is + positive increase te product items-quantity at the cart
       - if the quantity is - negitive increase te product items-quantity at the cart
    user can remove the product from the cart
    """
    serializer_class = CartItemSerializer
    permission_classes=[IsAuthenticated]
    lookup_field='product_pk'
    def get_queryset(self):
        user=self.request.user
        product_pk = self.kwargs.get('product_pk', None)
        query_set=CartItem.objects.filter(user=user)
        try:
            product = Product.objects.get(pk=product_pk)
        except Product.DoesNotExist:
            return None
        query_set=CartItem.objects.filter(user=user,product=product)
        return query_set
        
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # ignore DRY i don't wanna to write a guery to get the product for each action ,i use method and call it from each Action 
    def get_product(self):
        product_pk = self.kwargs.get('product_pk', None)
        try:
            product = Product.objects.select_for_update().get(pk=product_pk)# to lock the product avoiding critacl section
        except Product.DoesNotExist:
            return None
        return product

    # add product to the cart
    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            user=request.user
            try:

                product=self.get_product()
                if product is None:
                    return Response({"Not Found": "Product not Fount"}, status=status.HTTP_404_NOT_FOUND)
                CartItem.objects.get(user=user,product=product)
            except CartItem.DoesNotExist:
                serializer=self.get_serializer(data={'quantity':1},partial=True)
                new_stock_quantity= product.stock_quantity-1 
                if new_stock_quantity < 0:
                    return Response({"Error": "stock is empty"}, status=status.HTTP_400_BAD_REQUEST)
 
                if serializer.is_valid():
                    serializer.save(user=user,product=product,quantity=1)
                    product.stock = new_stock_quantity
                    product.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    transaction.set_rollback(True)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return super().create(request, *args, **kwargs)
            return Response({"Exist": "this product was add to Caart befor"}, status=status.HTTP_400_BAD_REQUEST)
   
    # update quantity for the product at the cart
    def update(self, request, *args, **kwargs):
        with transaction.atomic():
            user=request.user
            quantity=request.data.get("quantity")
            try:
                product=self.get_product()
                if product is None:
                    return Response({"Not Found": "Product not Fount"}, status=status.HTTP_404_NOT_FOUND)

                new_stock_quantity= product.stock_quantity-quantity
                if new_stock_quantity < 0:
                    return Response({"Error": "product does'nt have this quantity "}, status=status.HTTP_400_BAD_REQUEST)

                cart_item=CartItem.objects.get(user=user,product=product)
                updated_quantity=cart_item.quantity+quantity
                if updated_quantity<0:
                    return Response({"Error": "you don't have this quantatiy for this product at   the cart"}, status=status.HTTP_400_BAD_REQUEST) 
                
                cart_item.save()
                serializer=self.get_serializer(cart_item,data={'quantity':updated_quantity},partial=True)
                if serializer.is_valid():
                    serializer.save()
                    product.stock_quantity = new_stock_quantity
                    product.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except CartItem.DoesNotExist:
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    # remove the product from the cart
    
    def destroy(self, request, *args, **kwargs):
        user=request.user
        with transaction.atomic():
            try:
                product=self.get_product()
                if product is None:
                    return Response({"Not Found": "Product not Fount"}, status=status.HTTP_404_NOT_FOUND)   
                cart_item=CartItem.objects.get(user=user,product=product)
                new_stock_quantity= product.stock_quantity+cart_item.quantity
                product.stock_quantity=new_stock_quantity
                product.save()

                cart_item.delete()
                return Response({"ok":" you removed the product from the cart"}, status=status.HTTP_202_ACCEPTED)
            except CartItem.DoesNotExist:
                transaction.set_rollback(True)
                return Response({"Not Found": "CartItem not Exist"}, status=status.HTTP_404_NOT_FOUND)

  






  

  
   