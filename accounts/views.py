from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, GenericAPIView
from .models import AppUser
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

from .serializers import UserLoginSerializer


# Create your views here.
class RegisterNewAppUserView(CreateAPIView):
    queryset = AppUser.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()


class UserLoginView(CreateAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid() == False:
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


""" 
{
    "email":  "admin2@admin.admin",
    "password": "sayed111199"
}

 """
