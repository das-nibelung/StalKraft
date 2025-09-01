from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent", "is_active", "sort_order")
    list_filter = ("is_active", "parent")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("sort_order", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "unit",
        "in_stock",
        "brand",
        "gost",
        "created_at",
    )
    list_filter = ("category", "in_stock", "brand", "gost")
    search_fields = ("name", "slug", "description", "brand", "gost")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("category",)
