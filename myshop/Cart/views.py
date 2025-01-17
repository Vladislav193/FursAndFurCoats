from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartItemSerializers, CartSerializers


class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        cart, created = Cart.objects.filter(user=request.user)
        serializer = CartSerializers(cart, many=True)
        return Response(serializer.data)

    def create(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        seriliazer = CartItemSerializers(data=request.data)
        if seriliazer.is_valid():
            CartItem.objects.create(cart=cart, **seriliazer.validated_data)
            return Response(seriliazer.data, status=status.HTTP_201_CREATED)
        return Response(seriliazer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        cart, create = Cart.objects.get_or_create(user=request.user)
        try:
            item = CartItem.oblects.get(cart=cart, id=pk)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)