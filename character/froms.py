from django import forms
from character.models import Proficience, Skills, Status
from helper.models import WeaponsType 

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



# class ProficienceEditModelForm(forms.ModelForm):
#     class Meta:
#         model = Characters
#         fields = ['__all__']
#         filds = ['name', 'alias']#add no field
#         exclude = ['page'] #excluir do form

#         labels = {
#             'name':'character name',
#             'alias':'is know as'
#         }

