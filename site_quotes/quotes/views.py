from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .form import QuoteForm
from .models import Quote, Author, Tag


# Create your views here.

def main(request):
    quotes = Quote.objects.all()
    paginator = Paginator(quotes, 10)  # показывать по 10 записей на странице.

    page_number = request.GET.get('page')
    quotes_page = paginator.get_page(page_number)

    return render(request, 'quotes/index.html', {'quotes_page': quotes_page})


def quotes_by_tag(request, tag_name):
    quotes = Quote.objects.filter(tags__name=tag_name)
    paginator = Paginator(quotes, 10)  # показывать по 10 записей на странице.

    page_number = request.GET.get('page')
    quotes_page = paginator.get_page(page_number)

    return render(request, 'quotes/index.html', {'quotes_page': quotes_page})


def author_info(request, author_id):
    author = Author.objects.get(id=author_id)
    return render(request, 'quotes/author.html', {'author': author})


@login_required
def new_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote_text = form.cleaned_data['quote']
            # Extract and split the tags from the form data
            tags_name = form.cleaned_data['tags'].split(',')

            # Get or create the author from the form data
            author_name = form.cleaned_data['author']
            author, _ = Author.objects.get_or_create(fullname=author_name)

            # Create a new quote and associate it with the author
            quote = Quote(quote=quote_text, author=author)
            quote.save()

            # Set the tags for the new quote
            for tag_name in tags_name:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                quote.tags.add(tag)

            # Redirect the user to the home page
            return redirect('/')
    else:
        form = QuoteForm()
    return render(request, 'quotes/new_quote.html', {'form': form})
