from django import forms

from geography.models import Country, Fief, Local, Region, Settlement
from helper.models import Economy, Localization, Resource, SettlementType


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        exclude = ['slug','fk_book']


class RegionForm(forms.Form):
    name = forms.CharField(max_length=50)
    localization = forms.ModelMultipleChoiceField(
        queryset= Localization.objects.all(),
    )
    description = forms.CharField(widget=forms.Textarea(
        attrs={'cols': 30, 'rows': 5}), required=False)


class FiefForm(forms.Form):
    name = forms.CharField(max_length=50)
    localization = forms.ModelMultipleChoiceField(
        queryset= Localization.objects.all(),
    )
    size = forms.IntegerField(min_value=0, label='size of fief in sqare meters')
    description = forms.CharField(widget=forms.Textarea(
        attrs={'cols': 30, 'rows': 5}), required=False)


class SettlementForm(forms.Form):
    name = forms.CharField(max_length=50)
    population = forms.IntegerField(min_value=0)
    type = forms.ChoiceField(label='wht type of settlement is?',
        choices=SettlementType.objects.all().values_list('name', 'name'))
    # economy = forms.ChoiceField(
    #     choices=Economy.objects.all().values_list('id', 'name'))
    economy = forms.ModelMultipleChoiceField(
        queryset= Economy.objects.all(),
        #widget = forms.CheckboxSelectMultiple
       
    )
    localization = forms.ModelMultipleChoiceField(
        queryset= Localization.objects.all(),
    )
    description = forms.CharField(widget=forms.Textarea(
        attrs={'cols': 30, 'rows': 5}), required=False)


class LocalForm(forms.Form):
    name = forms.CharField(min_length=4)
    resource = forms.ModelMultipleChoiceField(
        required =False,
        queryset= Resource.objects.all())
    description = forms.CharField(max_length=50)
    localization = forms.ModelMultipleChoiceField(
        queryset= Localization.objects.all(),
    )
    description = forms.CharField(widget=forms.Textarea(
        attrs={'cols': 30, 'rows': 5}), required=False)
