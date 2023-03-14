from django import forms
from character.models import Characters, Inventory, Proficience, Skills, Status, CharacterSkills, CharacterRealm
from helper.models import WeaponsType
from utils.medidas import Monetary 

class ProfileForm(forms.Form):
    img = forms.FileField(allow_empty_file=True, required=False)


class CharacterForm(forms.ModelForm):
    class Meta:
        model=Characters
        exclude=['slug','skills','proficience','realm']


class CharacterRealmForm(forms.ModelForm):
    class Meta:
        model = CharacterRealm
        exclude = ['fk_character']


class ProficienceForm(forms.Form):
    weapon = forms.ChoiceField(label='arma de escolha', choices =WeaponsType.objects.all().values_list('id','weapon'))
    proficience = forms.ChoiceField(choices =Proficience.objects.all().values_list('id','rank'), )
    page = forms.IntegerField(min_value=0, error_messages={
        'required':'numero da pagina  não pode estar vazio'
    })
    level = forms.IntegerField(max_value=10, min_value=0)
    

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        exclude = ['fk_character']



class SkillForm(forms.ModelForm):
    class Meta:
        model = Skills
        fields = '__all__'


class CharacterSkillForm(forms.ModelForm):
    class Meta:
        model = CharacterSkills
        exclude = ['character_id']


# class ProficienceEditModelForm(forms.ModelForm):
#     class Meta:
#         model = Characters
#         fields = '__all__'
#         filds = ['name', 'alias']#add no field
#         exclude = ['page'] #excluir do form

#         labels = {
#             'name':'character name',
#             'alias':'is know as'
#         }

############################inventario#############################3

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