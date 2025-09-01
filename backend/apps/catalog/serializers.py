from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "description", "image", "parent", "url")

    def get_url(self, obj):
        return obj.get_absolute_url()


class ProductSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "image",
            "price",
            "unit",
            "in_stock",
            "brand",
            "length",
            "thickness",
            "gost",
            "category",
            "category_name",
            "url",
        )

    def get_url(self, obj):
        return obj.get_absolute_url()
