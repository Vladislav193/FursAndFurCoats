from rest_framework import serializers
from .models import Product, Category


class ProductSerializers(serializers.ModelSerializer):
    image = serializers.CharField(write_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'image', 'price', 'category', 'specifications']


class CategorySerializers(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent_category', 'children']

    def get_children(self, obj):
        if obj.children.exists():
            return CategorySerializers(obj.children.all(), many=True).data
        return []