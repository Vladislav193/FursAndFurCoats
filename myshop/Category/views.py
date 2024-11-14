from rest_framework import viewsets, filters, status
from rest_framework.response import Response
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


class ProductInCategoryViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        serializer = CategorySerializers(data=request.data)
        if serializer.is_valid():
            category_id = serializer.validated_data.get('name')
            products = Product.objects.filter(category__name=category_id)
            product_data = [
                {
                    'id': product.id,
                    'name': product.name,
                    'description': product.description,
                    'price': product.price,
                    'category': product.category.name,
                    'image': product.image.url if product.image else None,
                }
                for product in products
            ]
            return Response(product_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)