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
    author_choice = forms.ModelChoiceField(to_field_name='fullname', queryset=Author.objects.all(), widget=forms.Select(
        attrs={
            'id': 'author_choice',
            'class': 'form-control',
            'placeholder': 'Введите автора'
        }
    ), required=False)

    author_input = forms.CharField(widget=forms.TextInput(
        attrs={
            'id': 'authorInput',
            'class': 'form-control',
            'placeholder': 'Введите автора'
        }
    ), required=False
    )
    CHOICES = ("choice", "author_choice"), ("input", "author_input")
    check_author_group = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author_choice'].choices = [(author.fullname, author.fullname) for author in Author.objects.all()]

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('check_author_group') == "choice":
            cleaned_data["author"] = cleaned_data.get('author_choice')
        elif cleaned_data.get('check_author_group') == "input":
            try:
                cleaned_data["author"] = Author.objects.get(fullname=cleaned_data['author_input'])
            except Author.DoesNotExist:
                cleaned_data["author"] = None
        return cleaned_data


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
