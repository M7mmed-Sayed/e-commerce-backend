from django.contrib import admin
from django.urls import path

from .views import StripeCheckoutView, stripe_webhook, StripePeymentView

urlpatterns = [

    # categories apis

    path('stripe/', StripeCheckoutView.as_view(), name='stripe-checkout'),
    # path('stripe-payment/', StripePeymentView.as_view(),name='stripe-payment'),
    path('webhook/', stripe_webhook),  #

]
