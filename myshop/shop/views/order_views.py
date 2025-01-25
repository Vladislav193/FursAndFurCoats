from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from myshop.shop.models.order_models import Order, OrderItem
from Cart.models import Cart
from myshop.shop.serializers.order_serializers import OrderSerializers
from myshop.shop.utils.send_confirmation import send_order_confirmation
from django.db import transaction


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user)
        price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
        with transaction.atomic():
            order = Order.objects.create(user=request.user, price=price)
            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                )
                for item in cart.cartitem_set.all()
            ]
            OrderItem.objects.bulk_create(order_items)
            cart.delete()
        serializer = OrderSerializers(order)
        send_order_confirmation(order, price)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
