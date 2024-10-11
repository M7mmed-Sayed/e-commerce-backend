from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from ..models import Category
from rest_framework import status
from ..serializers import CategorySerializers
from accounts.models import UserType

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes=[AllowAny]

    #change the permission_classes by the Action
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    #  create filtarion by the name
    def list(self, request, *args, **kwargs):
        search = request.query_params.get('category', None) 
        if search:
            queryset = self.queryset.filter(name__icontains=search) 
        else:
            queryset = self.queryset 
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
       
    
    def create(self, request, *args, **kwargs):
        #check if the user is admin or Employees to create
        if request.user.usertype not in[ UserType.ADMIN,UserType.EMPLOYEE]:
            return Response({"Unauthorized": "only admins or Employees can create Category"},status=status.HTTP_401_UNAUTHORIZED)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        #check if the user is admin or Employees to update
        if request.user.usertype not in[ UserType.ADMIN,UserType.EMPLOYEE]:
            return Response({"Unauthorized": "only admins or Employees can edit Category"},status=status.HTTP_401_UNAUTHORIZED)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        #check if the user is admin or Employees  to update
        if request.user.usertype not in[ UserType.ADMIN,UserType.EMPLOYEE]:
            return Response({"Unauthorized": "only admins or Employees can delete Category"},status=status.HTTP_401_UNAUTHORIZED)
        return super().destroy(request, *args, **kwargs)
  
   