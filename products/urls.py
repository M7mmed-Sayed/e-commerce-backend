
from django.contrib import admin
from django.urls import path
from .views import CategoryViewSet,ProductViewSet
urlpatterns = [

   #categories apis
   path('categories/', CategoryViewSet.as_view({
        'get': 'list',
         'post': 'create'
    }),name='categories'),
     path('category/<int:pk>/', CategoryViewSet.as_view({
        'delete': 'destroy',  
        'put': 'update',  
         'get': 'retrieve',
    }),name='category-datial'),


    #--------------------------------
       path('', ProductViewSet.as_view({
        'get': 'list',
         'post': 'create'
    }),name='product'),
     path('<int:pk>', ProductViewSet.as_view({
        'delete': 'destroy',  
        'put': 'update',  
         'get': 'retrieve',
    }),name='product-datial')



]
