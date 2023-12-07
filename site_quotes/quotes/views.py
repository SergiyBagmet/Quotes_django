from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Quote


# Create your views here.

def main(request):
    quotes = Quote.objects.all()
    paginator = Paginator(quotes, 10)  # показывать по 10 записей на странице.

    page_number = request.GET.get('page')
    quotes_page = paginator.get_page(page_number)

    return render(request, 'quotes/index.html', {'quotes_page': quotes_page})
