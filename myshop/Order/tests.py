from Category.models import Product, Category
from .models import Cart, CartItem
from Order.models import Order
from rest_framework.test import APIClient
from django.contrib.auth.models import User
import pytest
from Users.models import User


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', email = "vladrosenrol@gmail.com", password = "vlad"
)


@pytest.fixture
def auth_token(client, user):
    response = client.post('/api/token/', {
        "email": "vladrosenrol@gmail.com",
        "password": "vlad"
    })
    return response.data['access']


@pytest.fixture
def category():
    return Category.objects.create(name='Fur Coats')


@pytest.fixture
def product(category):
    return Product.objects.create(
        name='Luxury Fur Coat',
        category=category,
        price=1000,
        specifications="High quality fur coat"
    )


@pytest.fixture
def cart(user):
    return Cart.objects.create(user=user)


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_create_order(cart, product, client, user,auth_token):
    client.login(username='testuser', password='vlad')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {auth_token}')

    CartItem.objects.create(cart=cart, product=product, quantity=1)

    response = client.post('/api/order/', {'cart_id': cart.id})

    assert response.status_code == 201
    assert Order.objects.filter(user=user).exists()

    assert CartItem.objects.filter(cart=cart).count() == 0
