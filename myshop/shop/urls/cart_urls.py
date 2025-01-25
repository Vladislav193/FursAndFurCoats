from rest_framework.routers import DefaultRouter
from myshop.shop.views.cart_views import CartViewSet

router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = router.urls