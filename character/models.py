from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from helper.models import  ItemType, WeaponsType, SkillMastery, Season, Periode

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


class Skills(models.Model):
    type_skill = models.CharField(max_length=20, choices=Rank().skill_type)
    weapon_type = models.SmallIntegerField( choices=WeaponsType.objects.all().values_list('id','weapon'))
    name = models.CharField(max_length=50)
    rank = models.CharField(max_length=20, choices=Rank().skill_rank)
    sub_rank = models.CharField(max_length=6, choices=Rank().skill_sub_rank)
    description = models.TextField()
    bonus_status = models.CharField(max_length=20)
    time = models.SmallIntegerField()
    bonus_1 = models.SmallIntegerField()
    bonus_2 = models.SmallIntegerField()
    bonus_3 = models.SmallIntegerField()
    bonus_4 = models.SmallIntegerField()
    bonus_5 = models.SmallIntegerField()

    def __str__(self):
        return f'{self.name} | {self.rank}'


class Proficience(models.Model):
    rank = models.CharField(max_length=20, choices=Rank().proficience_rank)
    learning = models.SmallIntegerField()
    damage = models.SmallIntegerField()
    control = models.SmallIntegerField()
    aura = models.SmallIntegerField(
         validators=[
            MinValueValidator(50)
        ]
    )


    def __str__(self):
        return f'{self.pk}: {self.rank} -- learning: {self.learning}% control:{self.control}'

class Realms(models.Model):
    rank_position = models.SmallIntegerField()
    rank = models.CharField(max_length=20, choices=realm)
    bonus_physic = models.SmallIntegerField()
    limit_spiritual = models.SmallIntegerField()
    bonus_spiritual = models.SmallIntegerField()
    limit_physic = models.SmallIntegerField()
    description = models.TextField(default='N/A')

    def __str__(self):
        return f'{self.rank_position}:{self.rank}   atritutos:{self.bonus_physic }/{self.limit_physic} |  atritutos_espitiruais:{self.bonus_spiritual }/{self.limit_spiritual}'

    class Meta:
        verbose_name_plural = 'Realms'



class Characters(models.Model):
    img = models.FileField(upload_to='images/character/', default='images/character/default.png')
    name = models.CharField(max_length=50)
    alias = models.CharField(max_length=50, default='N/A')
    birth_year = models.SmallIntegerField()
    season = models.ForeignKey(Season, on_delete=models.SET_NULL, null=True)
    periode = models.ForeignKey(Periode,on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(default='', blank=True, null=True, db_index=True)
    skills = models.ManyToManyField(Skills, through='CharacterSkills')
    proficience = models.ManyToManyField(Proficience, through='CharacterProficience')
    realm = models.ManyToManyField(Realms,through='CharacterRealm')
    description = models.TextField(default='olá eu sou goku', null=True)

    def save(self, *args, **kwargs):  # sobrescreve o save metod
        self.slug = slugify(f'{self.name} {self.alias} {self.birth_year} {self.pk}')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.pk} | {self.name}  {self.alias}'

    def get_absolute_url(self):
        return reverse('character-page', kwargs={'slug': self.slug})

    class Meta:
        verbose_name_plural = 'Character Entries'


class CharacterRealm(models.Model):
    fk_character = models.ForeignKey(Characters, on_delete=models.CASCADE)
    fk_realm = models.ForeignKey(Realms, on_delete=models.CASCADE)
    page = models.SmallIntegerField()

class CharacterSkills(models.Model):
    character_id = models.ForeignKey(Characters, on_delete=models.CASCADE)
    skill_id = models.ForeignKey(Skills, on_delete=models.CASCADE)
    mastery = models.ForeignKey(SkillMastery, on_delete=models.SET_DEFAULT, default=0)
    page = models.SmallIntegerField()

    class Meta:
        verbose_name_plural = 'character Skills'

    def __str__(self):
        return f' {self.pk} : {self.skill_id} | {self.mastery} page: {self.page}'


class CharacterProficience(models.Model):
    character_id = models.ForeignKey(Characters, on_delete=models.CASCADE)
    proficience_id = models.ForeignKey(Proficience, on_delete=models.CASCADE)
    weapon_id = models.ForeignKey(WeaponsType, on_delete=models.CASCADE)
    level = models.SmallIntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ])
    page = models.SmallIntegerField()

    def __str__(self):
        return f'{self.pk}: {self.weapon_id} | {self.proficience_id}'


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

    class Meta:
        verbose_name_plural = 'Status Entries'


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

    