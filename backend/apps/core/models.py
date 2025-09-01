from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail import blocks
from django.apps import apps


class HomePage(Page):
    hero_title = models.CharField("Заголовок Hero", max_length=255, blank=True)
    hero_subtitle = models.TextField("Подзаголовок Hero", blank=True)
    hero_button_text = models.CharField("Текст кнопки", max_length=100, blank=True)
    hero_button_anchor = models.CharField("Якорь кнопки", max_length=100, blank=True)

    hero_carousel = StreamField(
        [
            ("image", ImageChooserBlock(required=True, help_text="Слайд карусели")),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Слайды Hero",
    )

    body = StreamField(
        [
            (
                "rich_text",
                blocks.RichTextBlock(
                    features=["h2", "h3", "bold", "italic", "link", "ol", "ul"]
                ),
            ),
            ("image", ImageChooserBlock()),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Контент",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_title"),
                FieldPanel("hero_subtitle"),
                FieldPanel("hero_button_text"),
                FieldPanel("hero_button_anchor"),
                FieldPanel("hero_carousel"),
            ],
            heading="Hero",
        ),
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Главная страница"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        Post = apps.get_model("blog", "Post")  # ← вместо прямого импорта
        context["recent_posts"] = (
            Post.objects.filter(is_published=True).order_by("-published_at", "-id")[:3]
        )
        return context
