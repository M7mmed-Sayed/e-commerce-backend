from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from ..models import Product
from rest_framework import status
from ..serializers import ProductSerializer
from accounts.models import UserType
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # allow any to be the defauit and change it if we need
    permission_classes=[AllowAny]



    
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        # search with category id/s
        category_params = request.query_params.get('category',None)  
        # search with product name
        name = request.query_params.get('name', None)
        # get the min price if it's none set 0
        min_price = request.query_params.get('min-price', 0)
         # get the max price if it's none set MAX calue 30000
        max_price = request.query_params.get('max-price', 30000)
        # have category params
        if category_params:
            category_list=category_params.split(',')
            queryset = queryset.filter(category__id__in=category_list)
        # have name params
        if name:
            queryset = queryset.filter(name__icontains=name)
        # search with range price or search with the default valus
        queryset = queryset.filter(price__gte=min_price, price__lte=max_price)
        #update the serializer after filtteration
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




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
  

  
   