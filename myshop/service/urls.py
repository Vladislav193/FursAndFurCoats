from django.urls import path
from .views import telega_login

urlpatterns = [
    path('auth_telegram/', telega_login, name='auth_telegram')
]