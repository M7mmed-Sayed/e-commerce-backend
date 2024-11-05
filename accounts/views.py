from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, GenericAPIView
from .models import AppUser,OTP
from .serializers import UserSerializer, UserLoginSerializer, UserUpdateSerializer
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core import serializers
from rest_framework.viewsets import ModelViewSet
from django.core.mail import send_mail
from .serializers import UserLoginSerializer
from django.core.cache import cache
from .utility import verify_otp,generate_otp,otp_exp_date,send_mail_otp
from datetime import datetime,timedelta
from django.conf import settings
me=settings.EMAIL_HOST_USER
my_pass=settings.EMAIL_HOST_PASSWORD
# import the necessary components first
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.db import transaction
from django.utils import timezone

# Create your views here.

class RegisterNewAppUserView(CreateAPIView):
    queryset = AppUser.objects.all()
    serializer_class = UserSerializer
    lookup_field="pk"
    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer=self.get_serializer(data=request.data)
            email=request.data.get("email",None)
            name=request.data.get("first_name",None)
            if serializer.is_valid():
                serializer.save()
                generated_otp_code=generate_otp()
                new_otp=OTP(otp_email=email,otp_expired_at=otp_exp_date(),otp_code=generated_otp_code)
                send_mail_otp(email,name,generated_otp_code)
                new_otp.save()
                print(generated_otp_code)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                transaction.set_rollback(True)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
    def perform_create(self, serializer):
        serializer.save()


class UserLoginView(CreateAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email=request.data.get("email",None)
        if email is None:
            return Response({"email": "requird an email"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            login_user=AppUser.objects.get(email=email)
        except AppUser.DoesNotExist:
            return Response({'error': 'Invalid credentials Invalid Email or Password'},
                            status=status.HTTP_401_UNAUTHORIZED)

        cache_key = email
        curren_user = cache.get(cache_key)
        cur_login_attempt_num=0
        if curren_user:
            limit = curren_user.get("limit", 0)
            un_lock_date = curren_user.get("un_lock_date")
            cur_login_attempt_num=limit
            if cur_login_attempt_num == 3:
                cur_time=datetime.now()
                diff=un_lock_date-cur_time
                seconds_diff = int(diff.total_seconds())
                return Response({'try-agin': f"try  to login agin after {seconds_diff} secondy, you reached the max attempts {cur_login_attempt_num}"},
                            status=status.HTTP_401_UNAUTHORIZED)

                    

        if serializer.is_valid() == False:
            if curren_user:
                cache.delete(email)
            user_invalid_login={
                'limit':cur_login_attempt_num+1,
                'un_lock_date':datetime.now()+timedelta(seconds=120)
            }
            cache.set(cache_key, user_invalid_login, timeout=120 ) 
            return Response({'error': 'Invalid credentials Invalid Email or Password'},
                            status=status.HTTP_401_UNAUTHORIZED)
        response = {
            'message': 'successfully logged in',
            'user': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def logout(request):
    token = Token.objects.get(user=request.user)
    token.delete()
    return Response({"message": "Logged  out success"}, status=status.HTTP_200_OK)


class UserProfileView(RetrieveAPIView):
    queryset = AppUser.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, *args, **kwargs)
        return Response(serializer.data)

    def get_object(self):
        return self.request.user


class UserUpdateView(UpdateAPIView):
    queryset = AppUser.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'username'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if user.username != instance.username:
            return Response({"authorize": "You don't have permission for this user."},
                            status=status.HTTP_401_UNAUTHORIZED)

        return super().update(request, *args, **kwargs)


@api_view(['POST'])
def otp_active(request):
    email=request.data.get("email",None)
    otp=request.data.get("otp_code",None)
    if email is None or otp is None:
        return Response({"email-otp": "requerd data email and otp"}, status=status.HTTP_400_BAD_REQUEST)
    with transaction.atomic():
        try:
            otp_object=OTP.objects.get(otp_email=email)
            app_user=AppUser.objects.get(email=email)
            valid_otp=otp_object.otp_code
            expired_otp=otp_object.otp_expired_at
            time_now=timezone.now()
            if verify_otp(otp,valid_otp)==False:
                return Response({"invalid OTP": "Invalid"}, status=status.HTTP_400_BAD_REQUEST)
            
            if expired_otp< time_now:
                return Response({"expired otp": "expired"}, status=status.HTTP_400_BAD_REQUEST)
            app_user.is_active=True
            otp_object.delete()
            return Response({"verified": "thanks"}, status=status.HTTP_200_OK)

        except OTP.DoesNotExist:
            transaction.set_rollback(True)
            return Response({"invalid Email": "you have to sign up"}, status=status.HTTP_400_BAD_REQUEST)
        except AppUser.DoesNotExist:
            transaction.set_rollback(True)
            return Response({"invalid Email": "you have to sign up"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            transaction.set_rollback(True)
            print(e)
            return Response({"Exception": "you have to sign up"}, status=status.HTTP_400_BAD_REQUEST)

        

@api_view(['POST'])
def otp_refresh(request):
    email=request.data.get("email",None)
    if email is None :
        return Response({"email": "required data- email "}, status=status.HTTP_400_BAD_REQUEST)
    try:
        otp_object=OTP.objects.get(otp_email=email)
        app_user=AppUser.objects.get(email=email)
        generated_otp_code=generate_otp()
        generated_otp_date=otp_exp_date()
        otp_object.otp_expired_at=generated_otp_date
        otp_object.otp_code=generated_otp_code
        otp_object.save()
        
        #send_mail_otp(email,app_user.first_name,generated_otp_code)
        return Response({"message":"check your email with new otp"}, status=status.HTTP_200_OK)
    except OTP.DoesNotExist:
        return Response({"Exception": "you have to sign up"}, status=status.HTTP_400_BAD_REQUEST)
    except AppUser.DoesNotExist:
        return Response({"Exception": "you have to sign up"}, status=status.HTTP_400_BAD_REQUEST)

    





@api_view(['POST'])
def send_mail_test(request):
    subject = 'Test Email'
    message = 'This is a test email sent using SMTP in Django.'
    recipient_list = ['mohamedsayed1167@gmail.com']
    
    send_mail(subject=subject, message=message, recipient_list=recipient_list,fail_silently=False,from_email=None)
    return Response({"message": "send ok XD :)"}, status=status.HTTP_200_OK)
