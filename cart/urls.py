
from django.contrib import admin
from django.urls import path
from .views import CartItemViewSet,CheckOutOrderView,OrderViewSet
urlpatterns = [

   #categories apis

     path('item/<int:product_pk>/', CartItemViewSet.as_view({
        'delete': 'destroy',  
        'put': 'update',  
        'post': 'create',
        'get': 'list',
        
    }),name='cart-item'),
     path('item', CartItemViewSet.as_view({
        'get': 'list',
        
    }),name='cartitems'),
     path('checkout', CheckOutOrderView.as_view(),name='checkout'),
     path('orders', OrderViewSet.as_view({
        'get': 'list',
        
    }),name='orders'),
    path('orders/<int:pk>', OrderViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',  
    
    }),name='order-datail'),





]
