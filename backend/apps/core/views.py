from django.shortcuts import render
from django.http import HttpResponse


def quote_view(request):
    if request.method == "POST":
        # Логика обработки формы (например, сохранение данных или отправка email)
        return HttpResponse("Запрос на коммерческое предложение отправлен!")
    return render(request, "pages/quote.html")  # Шаблон для формы, если нужен


def custom_page_not_found(request, exception, template_name="404.html"):
    return render(request, template_name, status=404)
