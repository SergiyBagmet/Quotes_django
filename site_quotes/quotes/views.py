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
            tags_name = form.cleaned_data['tags'].split(',')

            # Get or redirect the author from the form data
            choice_button_pressed = form.cleaned_data['check_author_group']
            input_button_pressed = form.cleaned_data['check_author_group']

            author = None
            if choice_button_pressed:
                # The radio button was selected, so get the author from the database
                author = form.cleaned_data['author_choice']
            elif input_button_pressed:
                # The input button was selected, so check if the author exists in the database
                try:
                    author = Author.objects.get(fullname=form.cleaned_data['author_input'])
                except Author.DoesNotExist:
                    # The author was created, so save the form data and redirect to the author form
                    request.session['quote_text'] = quote_text
                    request.session['tags_name'] = tags_name
                    request.session['author_input'] = author.fullname
                    return redirect('quotes:new_author')

            # Create a new quote and associate it with the author
            quote = Quote(quote=quote_text, author=author)
            quote.save()

            # Set the tags for the new quote
            for tag_name in tags_name:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                quote.tags.add(tag)

            # Redirect the user to the home page
            messages.success(request, f"цитата добавлена")
            return redirect('/')
    else:
        # If the request is not a POST request, check if there is form data in the session
        if 'quote_text' in request.session:
            # If there is form data in the session, create a new form with the data
            form = QuoteForm(initial={
                'quote': request.session['quote_text'],
                'tags': ', '.join(request.session['tags_name']),
                'author_input': request.session['author_input'],
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
            if 'quote_text' in request.session:
                return redirect('new_quote/')
            else:
                return redirect('/')
    else:
        form = AuthorForm()
    return render(request, 'quotes/new_author.html', {'form': form})
