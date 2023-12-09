from urllib.request import Request

from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Quote, Author


# Create your views here.

def main(request):
    quotes = Quote.objects.all()
    paginator = Paginator(quotes, 10)  # показывать по 10 записей на странице.

    page_number = request.GET.get('page')
    quotes_page = paginator.get_page(page_number)

    return render(request, 'quotes/index.html', {'quotes_page': quotes_page})


def author_info(request, author_id):
    author = Author.objects.get(id=author_id)
    return render(request, 'quotes/author.html', {'author': author})
