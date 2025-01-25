from rest_framework.routers import DefaultRouter
from myshop.shop.views.order_views import OrderViewSet

router = DefaultRouter()
router.register(r'order', OrderViewSet)

urlpatterns = router.urls