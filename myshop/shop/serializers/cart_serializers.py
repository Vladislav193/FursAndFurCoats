from myshop.shop.models.cart_models import Cart
from rest_framework import serializers
from myshop.shop.models.cart_models import CartItem


class CartItemSerializers(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ['product_id', 'quantity']

    def create(self, validated_data):
        cart_item, created = CartItem.objects.get_or_create(
            cart=self.context['cart'],
            product=validated_data['product_id'],
            quantity=validated_data['quantity']
        )
        if not created:
            cart_item.quantity += validated_data['quantity']
            cart_item.save()
        return cart_item


class CartSerializers(serializers.ModelSerializer):
    items = CartItemSerializers(source='cartitem_set', many=True)
    class Meta:
        model = Cart
        fields = ['user', 'items']