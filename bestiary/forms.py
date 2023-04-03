from django import forms
from .models import Loot, MagicBeast, MagicBeastLoot



def magicbeast_form_type(post= None, file= None, type =None, model=None):
    class MagicBeastForm(forms.ModelForm):    
        class Meta:
            model = MagicBeast
            exclude = ['slug', 'fk_book']
        
        def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs)
            if type == 'murim':
                #caso seja murim, vou pedir para excluir os campos do fantasy
                self.fields.pop('fantasy_atribute')
            elif type == 'fantasy':
                self.fields.pop('murim_realm')
    beast = MagicBeastForm(post, file, instance=model)
    return beast




class LootForm(forms.ModelForm):
    class Meta:
        model = Loot
        exclude = ['fk_beast','fk_book']
        labels = {
            'value':'value in silver coins'
        }

class MonsterLootForm(forms.ModelForm):
    class Meta:
        model = MagicBeastLoot
        fields = ['filtred_loot','qtd_meter','qtd_kg']
    filtred_loot = forms.ModelChoiceField(
        queryset= Loot.objects.filter(fk_book__type = 'murim')
    )