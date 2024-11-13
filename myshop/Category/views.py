from rest_framework import viewsets, filters
from .models import Product, Category
from .serializers import ProductSerializers, CategorySerializers


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['category__name']
    ordering_fields = ['price']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(parent_category__isnull=True)
    serializer_class = CategorySerializers