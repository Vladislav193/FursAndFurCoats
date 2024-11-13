from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, ProductInCategoryViewSet

router = DefaultRouter()
router.register(r'product', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductInCategoryViewSet, basename='product_in_category')


urlpatterns =router.urls