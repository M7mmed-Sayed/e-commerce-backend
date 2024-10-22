
from rest_framework import filters
from ..models import Product
import django_filters
class ProductFilter(django_filters.FilterSet):
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte',label="less than or equal")
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gt',label="greater than")
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains',label="contains name")
    class Mate:
        model=Product

