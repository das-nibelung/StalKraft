from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

handler404 = "apps.core.views.custom_page_not_found"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cms/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("catalog/", include(("apps.catalog.urls", "catalog"), namespace="catalog")),
    path(
        "services/", include(("apps.services.urls", "services"), namespace="services")
    ),
    path("blog/", include(("apps.blog.urls", "blog"), namespace="blog")),
    path("delivery/", TemplateView.as_view(template_name="delivery.html")),
    path(
        "quality-standarts/",
        TemplateView.as_view(template_name="quality_standarts.html"),
    ),
    path("steel-types/", TemplateView.as_view(template_name="steel_types.html")),
    path(
        "aliminum-alloys/",
        TemplateView.as_view(template_name="aluminum_alloys.html"),
        name="aluminum_alloys",
    ),
    path(
        "stainless-steel/",
        TemplateView.as_view(template_name="stainless_steel.html"),
        name="stainless_steel",
    ),
    path(
        "certificates/",
        TemplateView.as_view(template_name="certificates.html"),
        name="certificates",
    ),
    path(
        "partners/",
        TemplateView.as_view(template_name="partners.html"),
        name="partners",
    ),
    path("career/", TemplateView.as_view(template_name="career.html"), name="career"),
    path("faq/", TemplateView.as_view(template_name="faq.html"), name="faq"),
    path("core/", include("apps.core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    re_path(r"", include(wagtail_urls)),
]
