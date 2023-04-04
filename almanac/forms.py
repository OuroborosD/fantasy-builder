from django import forms

from almanac.models import Almanac




class AlmanacForm(forms.ModelForm):
    class Meta:
        model = Almanac
        exclude = ['fk_book']
        