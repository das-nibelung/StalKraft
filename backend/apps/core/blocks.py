# apps/core/blocks.py
from wagtail.blocks import (
    StructBlock, StreamBlock, StreamBlockValidationError,
    CharBlock, RichTextBlock, URLBlock, ListBlock
)
from wagtail.images.blocks import ImageChooserBlock
from django.utils.module_loading import import_string

# ---------- Hero ----------
class HeroBlock(StructBlock):
    title = CharBlock(required=False, label="Заголовок")
    subtitle = RichTextBlock(required=False, features=["bold", "italic", "link"], label="Подзаголовок")
    button_text = CharBlock(required=False, default="Начать сотрудничество", label="Текст кнопки")
    button_anchor = CharBlock(required=False, default="#get-started", label="Якорь/ссылка кнопки (href)")
    slides = ListBlock(ImageChooserBlock(label="Слайд"), required=False, label="Слайды карусели")

    class Meta:
        icon = "image"
        template = "core/blocks/hero.html"
        label = "Герой (верх страницы)"

# ---------- Get Started (левая колонка + форма справа) ----------
class GetStartedBlock(StructBlock):
    left_title = CharBlock(required=False, label="Заголовок слева")
    left_text = RichTextBlock(required=False, features=["bold", "italic", "link", "ul"], label="Текст слева")
    form_action = CharBlock(required=False, default="contacts:quote", label="URL name формы (reverse)")

    class Meta:
        icon = "form"
        template = "core/blocks/get_started.html"
        label = "Get Started (форма КП)"

# ---------- Карточки продукции (2x2) ----------
class ProductCard(StructBlock):
    image = ImageChooserBlock(required=False, label="Картинка")
    title = CharBlock(label="Заголовок")
    text = RichTextBlock(required=False, features=["bold","italic"], label="Текст")

class ProductsSectionBlock(StructBlock):
    section_title = CharBlock(default="Наша продукция")
    section_subtitle = RichTextBlock(required=False, features=["italic"])
    cards = ListBlock(ProductCard, min_num=1, label="Карточки")

    class Meta:
        icon = "list-ul"
        template = "core/blocks/products_section.html"
        label = "Секция: продукция"

# ---------- Услуги ----------
class ServiceItem(StructBlock):
    icon_class = CharBlock(required=False, default="fa-solid fa-mountain-city", label="CSS-класс иконки")
    title = CharBlock()
    text = RichTextBlock(required=False, features=["italic"])

class ServicesSectionBlock(StructBlock):
    section_title = CharBlock(default="Услуги")
    section_subtitle = RichTextBlock(required=False, features=["italic"])
    items = ListBlock(ServiceItem, min_num=1, label="Услуги")

    class Meta:
        icon = "cog"
        template = "core/blocks/services_section.html"
        label = "Секция: услуги"

# ---------- Альт-сервисы (картинка слева + 4 пункта) ----------
class AdvantageItem(StructBlock):
    icon_class = CharBlock(required=False, default="bi bi-easel")
    title = CharBlock()
    text = RichTextBlock(required=False, features=["italic"])

class AltServicesBlock(StructBlock):
    bg_image = ImageChooserBlock(required=False, label="Фоновое изображение слева")
    title = CharBlock(default="Наши преимущества")
    intro = RichTextBlock(required=False, features=["italic"])
    items = ListBlock(AdvantageItem, min_num=1, max_num=6, label="Преимущества")

    class Meta:
        icon = "placeholder"
        template = "core/blocks/alt_services.html"
        label = "Альт-сервисы / Преимущества"

# ---------- Табы (любой набор) ----------
class FeatureTab(StructBlock):
    title = CharBlock(label="Заголовок таба")
    left = RichTextBlock(required=False, features=["bold","italic","link","ul"])
    right_image = ImageChooserBlock(required=False, label="Картинка справа")

class FeaturesTabsBlock(StructBlock):
    tabs = ListBlock(FeatureTab, min_num=1, label="Табы")

    class Meta:
        icon = "folder-open-inverse"
        template = "core/blocks/features_tabs.html"
        label = "Секция: табы"

# ---------- Проекты (портфолио) ----------
class ProjectItem(StructBlock):
    image = ImageChooserBlock(required=False)
    title = CharBlock()
    text = CharBlock(required=False)
    filter_class = CharBlock(required=False, help_text="CSS-класс фильтра, например: filter-industrial")

class ProjectsSectionBlock(StructBlock):
    section_title = CharBlock(default="Наши проекты")
    section_subtitle = RichTextBlock(required=False, features=["italic"])
    items = ListBlock(ProjectItem, min_num=1)

    class Meta:
        icon = "site"
        template = "core/blocks/projects_section.html"
        label = "Секция: проекты"

# ---------- Отзывы ----------
class TestimonialItem(StructBlock):
    image = ImageChooserBlock(required=False, label="Фото")
    name = CharBlock()
    role = CharBlock(required=False, label="Должность/компания")
    rating = CharBlock(required=False, default="★★★★★")
    text = RichTextBlock(required=True, features=["italic"])

class TestimonialsSectionBlock(StructBlock):
    section_title = CharBlock(default="Отзывы клиентов")
    section_subtitle = RichTextBlock(required=False, features=["italic"])
    items = ListBlock(TestimonialItem, min_num=1)

    class Meta:
        icon = "user"
        template = "core/blocks/testimonials_section.html"
        label = "Секция: отзывы"

# ---------- Новости (простая заглушка; можно заменить на автоподбор из блога) ----------
class NewsItem(StructBlock):
    image = ImageChooserBlock(required=False)
    date_text = CharBlock(required=False, default="15 октября")
    title = CharBlock()
    author = CharBlock(required=False)
    category = CharBlock(required=False)
    link = URLBlock(required=False)

class RecentNewsBlock(StructBlock):
    section_title = CharBlock(default="Последние новости")
    section_subtitle = RichTextBlock(required=False, features=["italic"])
    items = ListBlock(NewsItem, min_num=1, max_num=6)

    class Meta:
        icon = "doc-full"
        template = "core/blocks/recent_news.html"
        label = "Секция: новости"


class AutoRecentPostsBlock(StructBlock):
    count = IntegerBlock(default=3, min_value=1, max_value=12, label="Сколько постов")
    show_author = BooleanBlock(required=False, default=True, label="Показывать автора")
    show_category = BooleanBlock(required=False, default=True, label="Показывать категорию")
    section_title = CharBlock(required=False, default="Последние новости", label="Заголовок секции")
    section_subtitle = CharBlock(required=False, default="Свежие публикации из блога", label="Подзаголовок")

    class Meta:
        icon = "doc-full"
        template = "core/blocks/recent_posts_auto.html"
        label = "Секция: последние посты (авто)"

    # Единственная «магия»: собрать queryset и положить его в контекст шаблона
    def get_context(self, value, parent_context=None):
        ctx = super().get_context(value, parent_context=parent_context)
        limit = value.get("count", 3)

        posts = []
        # ---- ВАРИАНТ А: Django-модель apps.blog.models.Post ----
        try:
            Post = import_string("apps.blog.models.Post")
            qs = Post.objects.all()
            # если у тебя есть поля вроде "is_published" и "published_at" — раскомментируй/исправь:
            if hasattr(Post, "is_published"):
                qs = qs.filter(is_published=True)
            if hasattr(Post, "published_at"):
                qs = qs.order_by("-published_at")
            elif hasattr(Post, "created_at"):
                qs = qs.order_by("-created_at")
            posts = list(qs[:limit])
            ctx["posts"] = posts
            ctx["source"] = "django"
            return ctx
        except Exception:
            pass

        # ---- ВАРИАНТ Б: Wagtail-страницы BlogPage ----
        try:
            from wagtail.models import Page
            BlogPage = import_string("apps.blog.models.BlogPage")  # поправь путь, если другой
            qs = Page.objects.type(BlogPage).live().specific()
            # если в BlogPage есть date/first_published_at — сортируем
            if hasattr(BlogPage, "date"):
                qs = qs.order_by("-date")
            else:
                qs = qs.order_by("-first_published_at")
            posts = list(qs[:limit])
            ctx["posts"] = posts
            ctx["source"] = "wagtail"
            return ctx
        except Exception:
            pass

        # Если ни один вариант не сработал — пусть будет пусто
        ctx["posts"] = []
        ctx["source"] = "none"
        return ctx