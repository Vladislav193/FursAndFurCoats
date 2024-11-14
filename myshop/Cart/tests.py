from Category.models import Product, Category
from .models import Cart, CartItem
from rest_framework.test import APIClient
from django.contrib.auth.models import User
import pytest
from Users.models import User


@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        email = "vladrosenrol@gmail.com",
        password = "vlad"
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
def test_add_to_cart(product, cart, client, user, auth_token):
    client.login(username='testuser', password='vlad')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {auth_token}')

    response = client.post(f'/api/cart/', {'product_id': product.id, 'quantity': 1})

    assert response.status_code == 201
    assert CartItem.objects.filter(cart=cart, product=product).exists()
    cart_item = CartItem.objects.get(cart=cart, product=product)
    assert cart_item.quantity == 1