from Category.models import Product, Category
from rest_framework.test import APIClient
import pytest
from Users.models import User


@pytest.fixture
def client():
    return APIClient()

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

@pytest.mark.django_db
def test_user_login(client, user):
    response = client.post('/api/token/', {
    "email": "vladrosenrol@gmail.com",
    "password": "vlad"
})

    assert response.status_code == 200
    assert 'access' in response.data  # Проверка наличия access токена

    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')


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


@pytest.mark.django_db
def test_get_product_detail(product, client, auth_token):
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {auth_token}')
    response = client.get(f'/api/product/{product.id}/')
    print(f'{product.name}')

    assert response.status_code == 200
    assert response.data['name'] == product.name
    assert response.data['category'] == product.category.id
    assert response.data['price'] == product.price
    assert response.data['specifications'] == product.specifications