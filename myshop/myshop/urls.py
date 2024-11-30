from django.contrib import admin
from django.urls import path, include
from .schema_urls import schema_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Category.urls')),
    path('api/', include('Cart.urls')),
    path('api/', include('Order.urls')),
    path('api/', include('Users.urls')),
    path('api/', include('my_yookassa.urls')),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('accounts/', include('allauth.urls')),
]

