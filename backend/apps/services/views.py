from django.shortcuts import render, get_object_or_404
from .models import Service, AltServiceBlock, Testimonial


def services_list(request):
    services = Service.objects.filter(is_active=True)
    alt_blocks = AltServiceBlock.objects.filter(is_active=True)
    testimonials = Testimonial.objects.filter(is_active=True)
    return render(
        request,
        "pages/services/services_list.html",
        {"services": services, "alt_blocks": alt_blocks, "testimonials": testimonials},
    )


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    return render(request, "pages/services/service_detail.html", {"service": service})
