from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegisterUserSerializer
from rest_framework.response import Response
from rest_framework import status


class RegisterUserApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializers = RegisterUserSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({"message":"Пользователь успешно зарегистрирован"}, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)