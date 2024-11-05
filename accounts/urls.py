
from django.contrib import admin
from django.urls import path
from .views import RegisterNewAppUserView,logout,UserLoginView,UserProfileView,UserUpdateView,send_mail_test,otp_active,otp_refresh
urlpatterns = [
   path('register/', RegisterNewAppUserView.as_view(),name='register'),
   path('login/', UserLoginView.as_view(),name='login'),
   path('logout/', logout,name='logout'),
   path('otp-active/', otp_active,name='otp_active'),
   path('otp-resend/', otp_refresh,name='otp_resend'),
   path('sendmail/', send_mail_test,name='send_mail_test'),
   path('', UserProfileView.as_view(),name='profile'),
   path('update/<str:username>', UserUpdateView.as_view(),name='profile-update'),
]
