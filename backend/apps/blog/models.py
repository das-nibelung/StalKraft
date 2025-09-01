from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField("Название", max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:list") + f"?category={self.slug}"


class Tag(models.Model):
    name = models.CharField("Название", max_length=60, unique=True)
    slug = models.SlugField(max_length=80, unique=True, blank=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["name"]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:list") + f"?tag={self.slug}"
    
    
class Post(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    excerpt = models.TextField("Короткое описание", blank=True)
    content = models.TextField("Содержимое (HTML)")
    featured_image = models.ImageField("Обложка", upload_to="blog/", blank=True, null=True)

    author = models.ForeignKey(
        User, verbose_name="Автор", on_delete=models.SET_NULL, null=True, blank=True
    )
    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.SET_NULL,
        null=True, blank=True, related_name="posts"
    )
    tags = models.ManyToManyField(Tag, verbose_name="Теги", blank=True, related_name="posts")

    is_published = models.BooleanField("Опубликовано", default=True)
    published_at = models.DateTimeField("Дата публикации")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-published_at", "-id"]
        indexes = [
            models.Index(fields=["is_published", "published_at"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title, allow_unicode=True)
            cand = base
            i = 2
            while Post.objects.filter(slug=cand).exclude(pk=self.pk).exists():
                cand = f"{base}-{i}"
                i += 1
            self.slug = cand
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:detail", args=[self.slug])
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField("Имя", max_length=120)
    email = models.EmailField("Email")
    body = models.TextField("Комментарии")
    is_approved = models.BooleanField("Показывать", default=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    