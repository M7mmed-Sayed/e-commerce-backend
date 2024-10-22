from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from ..models import Product
from rest_framework import status
from ..serializers import ProductSerializer
from accounts.models import UserType
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from ..filter import ProductFilter
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related("category")
    serializer_class = ProductSerializer
    filter_backends = [
        DjangoFilterBackend,
    ]

    filterset_class = ProductFilter
    # allow any to be the defauit and change it if we need
    permission_classes=[AllowAny]
    #change the permission_classes by the Action
    def get_permissions(self):
        # method git any one can use
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        else:
            # must be Authenticated to do any thing else 
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]




    def create(self, request, *args, **kwargs):
         #check if the user is seller to add product
        if request.user.usertype not in[ UserType.SELLER]:
            return Response({"Unauthorized": "only admins or Employees can create Category"},status=status.HTTP_401_UNAUTHORIZED)
        return super().create(request, *args, **kwargs)





    def update(self, request, *args, **kwargs):
        #check if the user is seller or not
        if request.user.usertype not in[ UserType.SELLER]:
            return Response({"Unauthorized": "only seller can edit Product"},status=status.HTTP_401_UNAUTHORIZED)
        #check if the user requester(Authenticated) is seller to can edit
        if request.user!= self.get_object().seller:
                 return Response({"Unauthorized": "only owner product can do that"},status=status.HTTP_401_UNAUTHORIZED)
        return super().update(request, *args, **kwargs)


    def destroy(self, request, *args, **kwargs):
         #check if the user is seller or not
        if request.user.usertype not in[ UserType.SELLER]:
            return Response({"Unauthorized": "only admins or Employees can delete Product"},status=status.HTTP_401_UNAUTHORIZED)
        #check if the user requester(Authenticated) is seller to can destroy
        if request.user!= self.get_object().seller:
                 return Response({"Unauthorized": "only owner product can do that"},status=status.HTTP_401_UNAUTHORIZED)
        return super().destroy(request, *args, **kwargs)

    # to set the prodect's owner with the current request user
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
        return super().perform_create(serializer)
  

  
   