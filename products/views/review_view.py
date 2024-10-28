from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Review,Product
from rest_framework import status
from django.db import transaction
from cart.models import OrderItem
from ..serializers import ReviewSerializer



class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes=[IsAuthenticated]
    def get_product(self):
        product_pk = self.kwargs.get('product_pk', None)
        try:
            product = Product.objects.select_for_update().get(pk=product_pk)# to lock the product avoiding critacl section
        except Product.DoesNotExist:
            return None
        return product

    def create(self, request, *args, **kwargs):
        
        with transaction.atomic():
            
            user=request.user
            rating=request.data.get("rating")
            try:
                product=self.get_product()
                if product is None:
                    return Response({"Not Found": "------ Product not Fount----"}, status=status.HTTP_404_NOT_FOUND)
                Review.objects.get(customer=user,product=product)
            except Review.DoesNotExist:
                try:
                    orderItem=OrderItem.objects.filter(user=user,product=product).first()
                    if orderItem is None :
                        return Response({"buy it": "u have to buy"}, status=status.HTTP_400_BAD_REQUEST)
                    serializer=self.get_serializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save(customer=user,product=product)
                        product.rating = product.rating+rating
                        product.num_reviews=product.num_reviews+1
                        product.save()
                        raise 
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except:
                    transaction.set_rollback(True)
                    return Response({"exeption": "roll back"}, status=status.HTTP_400_BAD_REQUEST)
            
            

            return Response({"Exist": "you added review before"}, status=status.HTTP_400_BAD_REQUEST)
   

  

  
   