from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator

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


skill_mastery =(
    ('beggining','beggining'),
    ('intermediary','intermediary'),
    ('small completion','small completion'),
    ('great completion','great completion'),
    ('master','master'),
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
    name = models.CharField(max_length=50)
    alias = models.CharField(max_length=50, default='N/A')
    birth_year = models.SmallIntegerField()
    season = models.CharField(max_length=30)
    periode = models.CharField(max_length=15)
    slug = models.SlugField(default='', blank=True, null=True, db_index=True)
    

    def save(self, *args, **kwargs):  # sobrescreve o save metod
        self.slug = slugify(f'{self.name} {self.alias} {self.birth_year}')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}  {self.alias}'

    def get_absolute_url(self):
        return reverse('character-page', kwargs={'slug': self.slug})

    class Meta:
        verbose_name_plural = 'character entries'

class Proficience(models.Model):
    weapon = models.CharField(max_length=20, choices=weapon_list)
    mastery = models.CharField(max_length=15, choices=proficience_rank)
    level = models.SmallIntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ])
    page = models.SmallIntegerField()
    fk_character = models.ManyToManyField(Characters)

    def __str__(self):
        return f'{self.weapon} {self.mastery}'


class Status(models.Model):
    STR = models.SmallIntegerField()
    AGI = models.SmallIntegerField()
    DEX = models.SmallIntegerField()
    RES = models.SmallIntegerField()
    CON = models.SmallIntegerField()
    KY = models.SmallIntegerField()
    CTL = models.SmallIntegerField()
    PER = models.SmallIntegerField()
    page = models.SmallIntegerField()
    fk_character = models.ForeignKey(Characters, on_delete=models.CASCADE)

    def __str__(self):
        return f' {self.page} {self.fk_character}'


class Skills(models.Model):
    name = models.CharField(max_length=50)
    rank = models.CharField(max_length=20, choices=skill_rank)
    sub_rank = models.CharField(max_length=6, choices=skill_sub_rank)
    mastery = models.CharField(max_length=20, choices=skill_mastery)
    page = models.SmallIntegerField()
    fk_character = models.ForeignKey(Characters, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}  rank:{self.rank}-{self.sub_rank} maestria atual {self.mastery}'


class Rank(models.Model):
    rank = models.CharField(max_length=20, choices=realm)
    page = models.SmallIntegerField()
    fk_character = models.ManyToManyField(Characters)
