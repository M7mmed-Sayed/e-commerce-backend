from django.contrib import admin
from django.urls import path

from .views import AboutFooterView

urlpatterns = [

    # categories apis

    path('', AboutFooterView.as_view(), name='about'),
    # path('stripe-payment/', StripePeymentView.as_view(),name='stripe-payment'),

]
