from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("catalog/", include("apps.catalog.urls")),
    path("blog/", include("apps.blog.urls")),
    path("contacts/", include("apps.contacts.urls")),
]
