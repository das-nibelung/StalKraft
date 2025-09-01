from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField("Название", max_length=120, unique=True)
    slug = models.SlugField("Слаг", max_length=140, unique=True)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField(
        "Изображение", upload_to="categories/", blank=True, null=True
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Родитель",
    )
    is_active = models.BooleanField("Активна", default=True)
    sort_order = models.PositiveIntegerField("Сортировка", default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:category", args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Категория",
    )
    name = models.CharField("Наименование", max_length=200)
    slug = models.SlugField("Слаг", max_length=220, unique=True)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField(
        "Изображение", upload_to="products/", blank=True, null=True
    )

    price = models.DecimalField(
        "Цена", max_digits=12, decimal_places=2, null=True, blank=True
    )
    unit = models.CharField(
        "Ед. изм.", max_length=20, default="шт", help_text="Напр.: шт, м, т"
    )
    in_stock = models.BooleanField("В наличии", default=True)

    brand = models.CharField("Марка", max_length=120, blank=True)  # (или mark)
    length = models.DecimalField(
        "Длина, м", max_digits=8, decimal_places=2, null=True, blank=True
    )
    thickness = models.DecimalField(
        "Толщина, мм", max_digits=8, decimal_places=2, null=True, blank=True
    )
    gost = models.CharField("ГОСТ", max_length=120, blank=True)

    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["name"]),
            models.Index(fields=["price"]),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:product", args=[self.slug])
