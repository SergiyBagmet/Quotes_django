from django import forms

from .models import Author


class QuoteForm(forms.Form):
    quote = forms.CharField(widget=forms.Textarea(
        attrs={
            'id': 'quoteInput',
            'class': 'form-control',
            'rows': '3'
        }
    )
    )
    tags = forms.CharField(widget=forms.TextInput(
        attrs={
            'id': 'tagsInput',
            'class': 'form-control',
            'placeholder': 'Введите теги через запятую'
        }
    )
    )
    author_choice = forms.ModelChoiceField(queryset=Author.objects.all(), empty_label=None)

    author_input = forms.ChoiceField(widget=forms.TextInput(
        attrs={
            'id': 'authorInput',
            'class': 'form-control',
            'placeholder': 'Введите автора'
        }
     )
     )
    check_author_choice = forms.BooleanField(required=False)
    check_author_input = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author_choice'].choices = [(author.fullname, author.fullname) for author in Author.objects.all()]

    class Meta:
        model = Author
        fields = ['author_choice']


class AuthorForm(forms.Form):
    fullname = forms.CharField(widget=forms.TextInput(
        attrs={
            'id': 'Author_nameInput',
            'class': 'form-control',
            'placeholder': 'Имя автора'
        }
    )
    )
    born_date = forms.CharField(widget=forms.TextInput(
        attrs={
            'id': 'born_dateInput',
            'class': 'form-control',
            'placeholder': 'дата рождения'
        }
    )
    )
    born_location = forms.CharField(widget=forms.TextInput(
        attrs={
            'id': 'born_locationInput',
            'class': 'form-control',
            'placeholder': 'место рождения'
        }
    )
    )
    description = forms.CharField(widget=forms.Textarea(
        attrs={
            'id': 'descriptionInput',
            'class': 'form-control',
            'placeholder': 'краткая биография',
            'rows': '3'
        }
    )
    )
