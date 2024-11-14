from .models import Cart
from rest_framework import serializers
from .models import CartItem
from Category.models import Product

class CartItemSerializers(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ['product_id', 'quantity']

    def create(self, validated_data):
        product = Product.objects.get(id=validated_data['product_id'])
        cart_item = CartItem.objects.create(
            user=self.context['request'].user,
            product=product,
            quantity=validated_data['quantity']
        )
        return cart_item


class CartSerializers(serializers.ModelSerializer):
    items = CartItemSerializers(source='cartitem_set', many=True)
    class Meta:
        model = Cart
        fields = ['user', 'items']