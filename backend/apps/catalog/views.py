from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, View
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from .models import Category, Product
from .cart import Cart


# ========== УТИЛИТЫ ФИЛЬТРАЦИИ ==========
def filter_products(request: HttpRequest, qs):
    q = request.GET.get("q")
    if q:
        qs = qs.filter(
            Q(name__icontains=q)
            | Q(description__icontains=q)
            | Q(brand__icontains=q)
            | Q(gost__icontains=q)
        )

    # чекбокс "в наличии"
    if request.GET.get("in_stock"):
        qs = qs.filter(in_stock=True)

    # фильтр по списку категорий (на общей странице каталога)
    cats = request.GET.getlist("category")
    if cats:
        qs = qs.filter(category__slug__in=cats)

    # диапазоны
    def to_decimal(val):
        try:
            return float(val.replace(",", "."))
        except Exception:
            return None

    pmin = to_decimal(request.GET.get("price_min", ""))
    pmax = to_decimal(request.GET.get("price_max", ""))
    if pmin is not None:
        qs = qs.filter(price__gte=pmin)
    if pmax is not None:
        qs = qs.filter(price__lte=pmax)

    lmin = to_decimal(request.GET.get("length_min", ""))
    lmax = to_decimal(request.GET.get("length_max", ""))
    if lmin is not None:
        qs = qs.filter(length__gte=lmin)
    if lmax is not None:
        qs = qs.filter(length__lte=lmax)

    tmin = to_decimal(request.GET.get("thickness_min", ""))
    tmax = to_decimal(request.GET.get("thickness_max", ""))
    if tmin is not None:
        qs = qs.filter(thickness__gte=tmin)
    if tmax is not None:
        qs = qs.filter(thickness__lte=tmax)

    # сортировка
    sort = request.GET.get("sort")
    order_map = {
        "price_asc": "price",
        "price_desc": "-price",
        "name_asc": "name",
        "name_desc": "-name",
        "newest": "-created_at",
    }
    if sort in order_map:
        qs = qs.order_by(order_map[sort])

    return qs


def paginate(request: HttpRequest, qs, default_per_page=12):
    try:
        per_page = int(request.GET.get("per_page", default_per_page))
    except ValueError:
        per_page = default_per_page
    per_page = per_page if per_page in (12, 24, 36, 60) else default_per_page

    paginator = Paginator(qs, per_page)
    page = request.GET.get("page") or 1
    try:
        page_obj = paginator.page(page)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return paginator, page_obj


# ========== ВЬЮХИ ДЛЯ ШАБЛОНОВ ==========
def catalog_view(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.filter(is_active=True).order_by("sort_order", "name")
    products_qs = Product.objects.select_related("category").all()
    products_qs = filter_products(request, products_qs)
    paginator, page_obj = paginate(request, products_qs)

    ctx = {
        "categories": categories,
        "products": page_obj.object_list,
        "paginator": paginator,
        "page_obj": page_obj,
        "selected_categories": request.GET.getlist("category"),
        "per_page_options": [12, 24, 36, 60],
    }
    return render(request, "pages/catalog/catalog.html", ctx)


def category_view(request: HttpRequest, slug: str) -> HttpResponse:
    category = get_object_or_404(Category, slug=slug, is_active=True)
    categories = Category.objects.filter(is_active=True).order_by("sort_order", "name")

    products_qs = Product.objects.select_related("category").filter(category=category)
    products_qs = filter_products(request, products_qs)
    paginator, page_obj = paginate(request, products_qs)

    ctx = {
        "category": category,
        "categories": categories,  # для сайдбара чекбоксов
        "products": page_obj.object_list,
        "paginator": paginator,
        "page_obj": page_obj,
        "selected_categories": request.GET.getlist("category"),
        "per_page_options": [12, 24, 36, 60],
    }
    # можно использовать тот же шаблон, он уже поддерживает список категорий и фильтры
    return render(request, "pages/catalog/catalog.html", ctx)


class ProductDetailView(DetailView):
    model = Product
    template_name = "pages/catalog/product_detail.html"
    context_object_name = "product"


# ========== КОРЗИНА ==========
def cart_add(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseBadRequest("POST only")

    try:
        product_id = int(request.POST.get("product_id"))
        qty = int(request.POST.get("qty", "1"))
    except (TypeError, ValueError):
        return HttpResponseBadRequest("bad params")

    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.add(product.id, qty=qty)

    # возврат на страницу, откуда добавляли
    next_url = request.POST.get("next") or product.get_absolute_url()
    return redirect(next_url)
