from django import forms
from character.models import Inventory
from helper.models import SkillMastery

from murim.models import Atribute, CharacterProficience, CharacterRealm, CharacterSkills, Skills
from utils.medidas import Monetary




class AtributosForm(forms.ModelForm):
    class Meta:
        model = Atribute
        exclude = ['fk_character']


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skills
        fields = '__all__'
        labels = {
            'bonus_1':'bonus que ganha no estagio aprendiz',
            'bonus_2':'bonus que ganha no estagio usuario',
            'bonus_3':'bonus que ganha no estagio pequena enligamento ',
            'bonus_4':'bonus que ganha no estagio grande enligamento',
            'bonus_5':'bonus que ganha no estagio de mestre',
            'time':'tem maximo que a skills é ativa, em segundos: ',

        }
        #BOOK adicionado atributos a tag html
        #isso vai adcionar o onchaced=""> na tag html do select
        widgets = {
            'rank': forms.Select(attrs={'onchange': 'this.form.submit()'}),

        }
    def __init__(self, *args, **kwargs):
        change = kwargs.pop('bonus', {})
        super(SkillForm, self).__init__(*args, **kwargs)
        for field_name, label in change.items():
            if label:
                #ATENTION precisa transformar para string, pois caso for numero da erro
                if self.fields[field_name] == self.fields['duration']:
                    self.fields[field_name].label += f' max {str(label)} (S)'
                else:
                    self.fields[field_name].label += f' {str(label)}'






class CharacterSkillForm(forms.ModelForm):
    class Meta:
        model = CharacterSkills
        exclude = ['fk_character']
        widgets = {
            'mastery': forms.Select(),
        }
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #      #BOOK adicionado tooptip ao select
    #     #self.fields['mastery'].widget.Select = self.get_choices_with_tooltips()
    #     self.fields['mastery'].widget.attrs.update(self.get_widget_attrs())
    #     print(f'	linha 59-------arquivo: ------- valor:	')
    #     print(self.fields['mastery'].widget.attrs)
    #     print(f'	linha 59-------arquivo: ------- valor:	')
    # # #BOOK adicionado tooptip ao choice
    # # #ormierio pego o capo no innit
    # # def get_choices_with_tooltips(self):
    # #     choices = []
    # #     for obj in SkillMastery.objects.all():
    # #         value = obj.pk
    # #         label = str(obj)
    # #         tooltip = obj.description
    # #         attrs = {"data-toggle":"tooltip" ,'title': tooltip}
    # #         choices.append((value, label, attrs))
    # #         print(f'	linha 68-------arquivo: {choices}------- valor:	')
    # #     print(f'	linha 69-------arquivo: {choices}------- valor:	')
    # #     return choices
    
    
    # #BOOK adicionado tooptip ao select
    # #ormierio pego o capo no innit
    # def get_widget_attrs(self):
    #     attrs = {}
    #     for obj in SkillMastery.objects.all():
    #         tooltip = obj.description
    #         attrs[obj.pk] = { "data-toggle":"tooltip" ,"data-placement":"right", "title":"Tooltip on right"}
    #     return attrs


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