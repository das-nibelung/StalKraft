from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Service(models.Model):
    title = models.CharField("Название", max_length=150)
    slug = models.SlugField("Слаг", max_length=160, unique=True, blank=True)
    excerpt = models.TextField("Короткое описание", max_length=300, blank=True)
    content = models.TextField("Полное описание", blank=True)
    icon_class = models.CharField(
        "CSS-класс иконки (Bootstrap Icons)", max_length=100, default="bi bi-building"
    )
    image = models.ImageField(
        "Изображение", upload_to="services/", blank=True, null=True
    )
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Показывать", default=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:160]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("services:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class AltServiceBlock(models.Model):
    """Блок с картинкой и буллетами (как в секции 'Alternative Services')."""

    title = models.CharField("Заголовок", max_length=150)
    text = models.TextField("Текст")
    bullets = models.JSONField("Пункты списка", default=list, help_text="Список строк")
    image = models.ImageField(
        "Изображение", upload_to="services/alt/", blank=True, null=True
    )
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Показывать", default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Альтернативный блок"
        verbose_name_plural = "Альтернативные блоки"

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField("Имя", max_length=100)
    role = models.CharField("Роль/должность", max_length=100, blank=True)
    text = models.TextField("Отзыв")
    avatar = models.ImageField(
        "Аватар", upload_to="services/testimonials/", blank=True, null=True
    )
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Показывать", default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return self.name
