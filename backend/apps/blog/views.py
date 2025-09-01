from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.db.models import Count, Q
from .models import Post, Category, Tag, Comment

POSTS_PER_PAGE = 9
RECENT_COUNT = 5


def _sidebar_context():
    categories = Category.objects.annotate(
        num_posts=Count("posts", filter=Q(posts__is_published=True))
    ).order_by("name")

    recent = (
        Post.objects.filter(is_published=True)
        .select_related("category", "author")
        .order_by("-published_at", "-id")[:RECENT_COUNT]
    )

    tags = Tag.objects.annotate(
        num_posts=Count("posts", filter=Q(posts__is_published=True))
    ).order_by("-num_posts", "name")[:30]

    return {
        "blog_categories": categories,
        "blog_recent_posts": recent,
        "blog_tags": tags,
    }


def blog_list(request):
    q = request.GET.get("q", "").strip()
    cat_slug = request.GET.get("category", "").strip()
    tag_slug = request.GET.get("tag", "").strip()

    qs = (
        Post.objects.filter(is_published=True)
        .select_related("author", "category")
        .prefetch_related("tags")
        .order_by("-published_at", "-id")
    )

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(excerpt__icontains=q) | Q(content__icontains=q))

    if cat_slug:
        qs = qs.filter(category__slug=cat_slug)

    if tag_slug:
        qs = qs.filter(tags__slug=tag_slug)

    paginator = Paginator(qs, POSTS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    ctx = {
        "posts": page_obj.object_list,
        "page_obj": page_obj,
        "paginator": paginator,
        "is_paginated": page_obj.has_other_pages(),
        "request": request,
        **_sidebar_context(),
    }
    return render(request, "blog/blog_list.html", ctx)


def blog_detail(request, slug):
    post = get_object_or_404(
        Post.objects.select_related("author", "category").prefetch_related("tags"),
        slug=slug,
        is_published=True,
    )

    comments = list(
        Comment.objects.filter(post=post, is_approved=True).order_by("created_at")
    )

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        body = request.POST.get("body", "").strip()
        if name and email and body:
            Comment.objects.create(post=post, name=name, email=email, body=body, is_approved=True)
            return redirect(post.get_absolute_url() + "#comments")

    ctx = {
        "post": post,
        "comments": comments,
        **_sidebar_context(),
    }
    return render(request, "blog/blog_detail.html", ctx)
