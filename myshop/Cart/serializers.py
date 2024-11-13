#from rest_framework import serializers
from .models import Cart, CartItem
#from Category.serializers import ProductSerializers


from rest_framework import serializers
from .models import CartItem
from Category.models import Product

class CartItemSerializers(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)  # Принимаем только ID продукта
    quantity = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ['product_id', 'quantity']

    def create(self, validated_data):
        # Получаем объект Product по переданному product_id
        product = Product.objects.get(id=validated_data['product_id'])
        # Создаем объект CartItem, используя найденный объект Product
        cart_item = CartItem.objects.create(
            user=self.context['request'].user,
            product=product,
            quantity=validated_data['quantity']
        )
        return cart_item

# class CartItemSerializers(serializers.ModelSerializer):
#     product = ProductSerializers()
#     class Meta:
#         model = CartItem
#         fields = ['product', 'quantity']


class CartSerializers(serializers.ModelSerializer):
    items = CartItemSerializers(source='cartitem_set', many=True)
    class Meta:
        model = Cart
        fields = ['user', 'items']


