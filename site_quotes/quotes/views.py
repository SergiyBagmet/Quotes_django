from django.shortcuts import render
from .models import Quote


# Create your views here.

def main(request):
    quotes = Quote.objects.all()
    return render(request, 'quotes/index.html', context={'quotes': quotes})
