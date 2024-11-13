from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from Cart.models import Cart
from .serializers import OrderSerializers
from .utils import send_order_confirmation


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user)
        price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
        order = Order.objects.create(user=request.user, price=price)
        for item in cart.cartitem_set.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
            cart.cartitem_set.clear()
            serializer = OrderSerializers(order)
            send_order_confirmation(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)