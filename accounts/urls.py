
from django.contrib import admin
from django.urls import path
from .views import RegisterNewAppUserView,logout,UserLoginView,UserProfileView,UserUpdateView
urlpatterns = [
   path('register/', RegisterNewAppUserView.as_view(),name='register'),
   path('login/', UserLoginView.as_view(),name='login'),
   path('logout/', logout,name='logout'),
   path('', UserProfileView.as_view(),name='profile'),
   path('update/<str:username>', UserUpdateView.as_view(),name='profile-update'),
]
