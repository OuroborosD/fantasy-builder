from django import forms

from helper.models import Books



class AddBookForm(forms.ModelForm):
    class Meta:
        model =  Books
        exclude = ['colection','slug']
        