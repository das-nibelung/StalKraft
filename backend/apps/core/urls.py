from django.urls import path
from django.views.generic import TemplateView
from .views import quote_view

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    path("quote/", quote_view, name="quote"),
]
