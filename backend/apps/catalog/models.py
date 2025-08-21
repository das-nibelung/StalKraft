from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="catalog/images/")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
