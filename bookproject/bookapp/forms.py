from django import forms
from .models import Book, Author


class AuthorForm(forms.ModelForm):

# to inform additional information in to the form
    class Meta:
        model = Author
        fields =['name']

class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = '__all__'
