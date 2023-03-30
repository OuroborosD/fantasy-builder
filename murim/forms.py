from django import forms
from character.models import Inventory

from murim.models import Atribute, CharacterProficience, CharacterRealm, CharacterSkills, Skills
from utils.medidas import Monetary




class AtributosForm(forms.ModelForm):
    class Meta:
        model = Atribute
        exclude = ['fk_character', 'KY']

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skills
        fields = '__all__'
        labels = {
            'bonus_1':'bonus que ganha no estagio aprendiz',
            'bonus_2':'bonus que ganha no estagio usuario',
        }

class CharacterSkillForm(forms.ModelForm):
    class Meta:
        model = CharacterSkills
        exclude = ['fk_character']

class CharacterRealmForm(forms.ModelForm):
    class Meta:
        model = CharacterRealm
        exclude = ['fk_character']


class CharacterProficienceForm(forms.ModelForm):
    class Meta:
        model = CharacterProficience
        exclude = ['fk_character']




# ############################inventario#############################3

class InventaryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        exclude = ['fk_character']
        labels = {
            'fk_item_type':'tipo'
        }
        widgets = {
            'description': forms.Textarea(attrs={'cols': 30, 'rows': 10}),
        }


class GoldForm(forms.Form):
    coin = forms.ChoiceField(label='coin type' ,choices=Monetary.type_coins, initial= 1)
    value = forms.FloatField()
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 20, 'rows': 5}), required=False)
    page = forms.IntegerField(min_value=0)