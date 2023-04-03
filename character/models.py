from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings
from core import settings

from PIL import Image
import os

from django.core.validators import MaxValueValidator, MinValueValidator
from helper.models import  Books, ItemType, WeaponsType, SkillMastery, Season, Periode

from utils.rank import Rank
# Create your models here.


############################# listas####################################
skill_rank = (
    ('comum', 'comum'),
    ('incomum', 'incomum'),
    ('rara', 'rara'),
    ('ancia', 'ancia'),
    ('legendaria', 'legendaria'),
    ('cobre', 'cobre'),
    ('ferro', 'ferro'),
    ('prata', 'prata'),
    ('ouro', 'ouro'),
    ('ferro negro', 'ferro negro'),
    ('ouro de iril', 'ouro de iril'),
    ('ferro vulcanico', 'ferro vulcanico'),
    ('bronze selestial', 'bronze selestial'),
    ('alomanium', 'alomanium'),
    ('frost metal', 'metal gelico'),
    ('abyss silver', 'prata abrissal'),
    ('metal morilitico', 'metal morilitico'),
    ('draconian steel', 'aço draconiana'),
    ('mitril', 'mitril'),
)

skill_sub_rank = (
    ('low', 'low'),
    ('middle', 'middle'),
    ('upper', 'upper'),
    ('peak', 'peak'),
)


skill_mastery = (
    ('beggining', 'beggining'),
    ('intermediary', 'intermediary'),
    ('small completion', 'small completion'),
    ('great completion', 'great completion'),
    ('master', 'master'),
)


proficience_rank = (
    ('apprentice', 'apprentice'),
    ('user', 'user'),
    ('fighter', 'fighter'),
    ('warrior', 'warrior'),
    ('veteran', 'veteran'),
    ('master', 'master'),
    ('gran-master', 'gran-master'),
    ('king', 'king'),
    ('emperor', 'emperor'),
    ('saint', 'saint'),
)


realm = (
    ('gate', 'gate'),
    ('garthering', 'garthering'),
    ('growing', 'growing'),
    ('control', 'control'),
    ('small-opening', 'small-opening'),
    ('fundation', 'fundation'),
    ('reforje', 'reforje'),
    ('revitalization', 'revitalization'),
    ('gran-opening', 'gran-opening'),
    ('rebirth', 'rebirth'),
    ('contruction', 'contruction'),
    ('espititualization', 'espititualization'),
    ('elementarization', 'elementarization'),
    ('elemetal mastery', 'elemetal mastery'),
    ('elemental king', 'elemental king'),

)

weapon_list = (
    ('sword', 'sword'),
    ('spear', 'spear'),
    ('axe', 'axe'),
    ('dagger', 'dagger'),
    ('bow', 'bow'),
    ('unarmed', 'unarmed'),
    ('shield', 'shield'),
    ('mace', 'mace'),
)

##########################################################################





class Characters(models.Model):
    fk_book = models.ForeignKey(Books, on_delete=models.SET_NULL, null=True)
    img = models.ImageField(upload_to='images/character/%Y/%m/%d/', default='images/default/character.png')
    name = models.CharField(max_length=50)
    alias = models.CharField(max_length=50, default='N/A')
    alive = models.CharField(max_length=20, choices=(('alive','alive'),('death','death')))
    birth_year = models.SmallIntegerField()
    season = models.ForeignKey(Season, on_delete=models.SET_NULL, null=True)
    periode = models.ForeignKey(Periode,on_delete=models.SET_NULL, null=True)
    description = models.TextField(default='olá eu sou goku', null=True)
    slug = models.SlugField(default='', blank=True, null=True, db_index=True)

    @staticmethod
    def resizeImg(img):
        print(f'	linha 121-------arquivo:   ------- valor:{img.url}	')
        #pega o caminho completo
        full_path = os.path.join(settings.MEDIA_ROOT , img.name)
        #chama o pilo e passa  caminho da imagem
        img_pillow = Image.open(full_path)
        #muda o tamanho da imagem
        width, heigth = img_pillow.size
        if width <= 350:
            img_pillow.close()
            return 
        new_img = img_pillow.resize((350,480), Image.LANCZOS)
        new_img.save(
            full_path,
        optimize=True,
                 )
        return
    def save(self, *args, **kwargs):  # sobrescreve o save metod
        
        self.slug = slugify(f'{self.name} {self.alias} {self.birth_year} {self.pk}')
        #salva  o registro primeiro, e depois consegue redimencionar
        saved = super().save(*args, **kwargs)
        if self.img:
            self.resizeImg(self.img)

        return saved

    def __str__(self):
        return f'{self.pk} | {self.name}  {self.alias}'
   


    class Meta:
        verbose_name_plural = 'Character Entries'

    




# class Skills(models.Model):
#     name = models.CharField(max_length=50)
#     rank = models.CharField(max_length=20, choices=skill_rank)
#     sub_rank = models.CharField(max_length=6, choices=skill_sub_rank)
#     mastery = models.CharField(max_length=20, choices=skill_mastery)
#     page = models.SmallIntegerField()
#     fk_character = models.ForeignKey(Characters, on_delete=models.CASCADE)

#     def __str__(self):
#         return f'{self.name}  rank:{self.rank}-{self.sub_rank} maestria atual {self.mastery}'




class Inventory(models.Model):
    fk_character = models.ForeignKey(Characters, on_delete= models.CASCADE)
    fk_item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True, blank=True)
    page = models.SmallIntegerField()



class GoldEntries(models.Model):
    fk_character = models.ForeignKey(Characters, on_delete=models.CASCADE)
    value = models.FloatField()
    description = models.CharField(max_length=200, blank=True, null=True)
    page = models.PositiveSmallIntegerField()

class TotalGold(models.Model):
    fk_character = models.ForeignKey(Characters, on_delete=models.CASCADE)
    value = models.FloatField()
    updated_page = models.PositiveSmallIntegerField()

    