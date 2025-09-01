from django.urls import path, include
from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.catalog_view, name="list"),  # /catalog/
    path("category/<slug:slug>/", views.category_view, name="category"),
    path("product/<slug:slug>/", views.ProductDetailView.as_view(), name="product"),
    path("cart/add/", views.cart_add, name="cart_add"),
]

# ---- API (DRF) ----
try:
    from rest_framework import routers, viewsets
    from .models import Category, Product
    from .serializers import CategorySerializer, ProductSerializer

    class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
        queryset = Category.objects.filter(is_active=True)
        serializer_class = CategorySerializer
        lookup_field = "slug"

    class ProductViewSet(viewsets.ReadOnlyModelViewSet):
        queryset = Product.objects.select_related("category").all()
        serializer_class = ProductSerializer
        lookup_field = "slug"

    router = routers.DefaultRouter()
    router.register(r"categories", CategoryViewSet, basename="category")
    router.register(r"products", ProductViewSet, basename="product")

    urlpatterns += [path("api/", include(router.urls))]
except Exception:
    # DRF не установлен — API просто не подключаем
    pass
