# apps/catalog/apps.py
from django.apps import AppConfig


class CatalogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.catalog"  # путь к модулю
    label = "catalog"  # метка приложения => таблицы catalog_*
    verbose_name = "Каталог"
