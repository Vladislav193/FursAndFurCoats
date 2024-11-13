import base64
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from .models import Product, Category

class ProductSerializers(serializers.ModelSerializer):
    image = serializers.CharField(write_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'image', 'price', 'category', 'specifications']

        def create(self, validated_data):
            # Декодируем Base64 изображение
            image_data = validated_data.pop('image')
            image_file = self.decode_base64_image(image_data)

            # Создаем продукт
            product = Product.objects.create(**validated_data, image=image_file)
            return product

        def decode_base64_image(self, base64_string):
            # Преобразуем строку Base64 в байты
            image_data = base64.b64decode(base64_string)
            # Конвертируем байты в файл
            return InMemoryUploadedFile(BytesIO(image_data), None, 'image.jpg', 'image/jpeg', len(image_data), None)


class CategorySerializers(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent_category', 'children']

    def get_children(self, obj):
        if obj.children.exists():
            return CategorySerializers(obj.children.all(), many=True).data
        return []


