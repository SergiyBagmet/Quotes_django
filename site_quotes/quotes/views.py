from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .form import QuoteForm, AuthorForm
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
            tags_name = [tag_name.strip() for tag_name in form.cleaned_data['tags'].split(',')]

            # Get or redirect the author from the form data
            if form.cleaned_data['author'] is None:
                request.session['quote'] = form.cleaned_data['quote']
                request.session['tags'] = form.cleaned_data['tags']
                request.session['check_author_group'] = form.cleaned_data['check_author_group']
                request.session['author_input'] = form.cleaned_data['author_input']
                return redirect('quotes:new_author')

            # Create a new quote and associate it with the author
            quote = Quote(quote=quote_text, author=form.cleaned_data['author'])
            quote.save()

            # Set the tags for the new quote
            for tag_name in tags_name:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                quote.tags.add(tag)

            # Redirect the user to the home page
            messages.success(request, f"цитата добавлена")
            del request.session['quote']
            del request.session['tags']
            del request.session['author_input']
            del request.session['check_author_group']
            return redirect('/')
    else:
        # If the request is not a POST request, check if there is form data in the session
        if 'author_input' in request.session:
            # If there is form data in the session, create a new form with the data
            form = QuoteForm(initial={
                'quote': request.session['quote'],
                'tags': request.session['tags'],
                'author_input': request.session['author_input'],
                'check_author_group': request.session['check_author_group'],
            })
        else:
            # If there is no form data in the session, create a new empty form
            form = QuoteForm()
    return render(request, 'quotes/new_quote.html', {'form': form})


@login_required
def new_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = Author(**form.cleaned_data)
            author.save()
            messages.success(request, f"автор добавлен")
            if 'author_input' in request.session:
                return redirect('quotes:new_quote')
            else:
                return redirect('/')
    else:
        if 'author_input' in request.session:
            form = AuthorForm(initial={
                'fullname': request.session['author_input'],
            })
        else:
            form = AuthorForm()
    return render(request, 'quotes/new_author.html', {'form': form})
