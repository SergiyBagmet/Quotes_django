from django import forms


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
    author = forms.CharField(widget=forms.TextInput(
        attrs={
            'id': 'authorInput',
            'class': 'form-control',
            'placeholder': 'Введите автора'
            }
        )
    )

