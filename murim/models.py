from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from character.models import Characters


from helper.models import SkillMastery, WeaponsType
from utils.rank import Rank

class AtributesDescription(models.Model):
    name =  models.CharField(max_length=15)
    description = models.TextField()

    def __str__(self):
        return f'{self.name} '

class SkillRank(models.Model):
    name = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null= True  , blank=True)
    multiplier = models.PositiveSmallIntegerField(null= True , blank=True)
    max_atributes = models.PositiveSmallIntegerField(null= True , blank=True)
    time = models.PositiveSmallIntegerField(null= True , blank=True)
    ky = models.PositiveSmallIntegerField(null= True , blank=True)

    def __str__(self):
        return f'{self.name} '

# Create your models here.
class Skills(models.Model):
    type_skill = models.CharField(max_length=20, choices=Rank().skill_type)
    weapon_type = models.ForeignKey(WeaponsType, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    rank = models.ForeignKey(SkillRank, on_delete=models.SET_NULL, null=True)
    sub_rank = models.CharField(max_length=6, choices=Rank().skill_sub_rank)
    description = models.TextField()
    atributes = models.ManyToManyField(AtributesDescription)
    time = models.SmallIntegerField(null= True, blank=True)
    bonus_1 = models.SmallIntegerField(null= True, blank=True)
    bonus_2 = models.SmallIntegerField(null= True, blank=True)
    bonus_3 = models.SmallIntegerField(null= True ,blank=True)
    bonus_4 = models.SmallIntegerField(null= True, blank=True)
    bonus_5 = models.SmallIntegerField(null= True, blank=True)

    def __str__(self):
        return f'{self.name} | {self.rank}'


class CharacterSkills(models.Model):
    fk_skill = models.ForeignKey(Skills, on_delete=models.CASCADE)
    fk_character = models.ForeignKey(Characters, on_delete=models.CASCADE)
    mastery = models.ForeignKey(SkillMastery, on_delete=models.SET_DEFAULT, default=0)
    page = models.SmallIntegerField()

    class Meta:
        verbose_name_plural = 'character Skills'

    def __str__(self):
        return f' {self.pk} :  | {self.mastery} page: {self.page}'

    class Meta:
        verbose_name_plural = 'Character Skills'
        #BOOK adicionar ordem
        ordering = ['-mastery']


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
    description = models.TextField(null=True)


    def __str__(self):
        return f'{self.pk}: {self.rank} -- learning: {self.learning}% control:{self.control}'


class CharacterProficience(models.Model):
    fk_character = models.ForeignKey(Characters, on_delete=models.CASCADE)
    fk_proficience = models.ForeignKey(Proficience, on_delete=models.CASCADE)
    weapon_id = models.ForeignKey(WeaponsType, on_delete=models.CASCADE)
    level = models.SmallIntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ])
    page = models.SmallIntegerField()

    def __str__(self):
        return f'{self.pk}: {self.weapon_id} '




class Realms(models.Model):
    rank_position = models.SmallIntegerField()
    rank = models.CharField(max_length=20)
    bonus_physic = models.SmallIntegerField()
    limit_spiritual = models.SmallIntegerField()
    bonus_spiritual = models.SmallIntegerField()
    limit_physic = models.SmallIntegerField()
    description = models.TextField(default='N/A')

    def __str__(self):
        return f'{self.rank_position}:{self.rank}   atritutos:{self.bonus_physic }/{self.limit_physic} |  atritutos_espitiruais:{self.bonus_spiritual }/{self.limit_spiritual}'

    class Meta:
        verbose_name_plural = 'Realms'
        #BOOK adicionar ordem
        ordering = ['rank_position']


class CharacterRealm(models.Model):
    fk_character = models.ForeignKey(Characters, on_delete=models.CASCADE, null=True)
    fk_realm = models.ForeignKey(Realms, on_delete=models.CASCADE)
    rank = models.CharField(choices=(('beggin','beggin',),('middle','middle'), ('upper','upper'), ('peak','peak')), max_length=15)
    page = models.SmallIntegerField()




class Atribute(models.Model):
    STR = models.SmallIntegerField(default=0)
    AGI = models.SmallIntegerField(default=0)
    DEX = models.SmallIntegerField(default=0)
    RES = models.SmallIntegerField(default=0)
    CON = models.SmallIntegerField(default=0)
    KY = models.SmallIntegerField(default=0)
    CTL = models.SmallIntegerField(default=0)
    PERCEPTION = models.SmallIntegerField(default=0)
    page = models.SmallIntegerField(default=0)
    fk_character = models.ForeignKey(Characters, on_delete=models.CASCADE)

    def __str__(self):
        return f' {self.page} {self.fk_character}'

    class Meta:
        verbose_name_plural = 'Atributes'







class Murim(models.Model):
    fk_character = models.ForeignKey(Characters, on_delete=models.CASCADE, null=True)
    fk_status = models.ForeignKey(Atribute, on_delete=models.SET_NULL, null=True)
    fk_proficience = models.ForeignKey(CharacterProficience, on_delete=models.SET_NULL, null=True)
    fk_skill = models.ForeignKey(CharacterSkills, on_delete=models.SET_NULL, null=True)
    fk_realm = models.ForeignKey(CharacterRealm, on_delete=models.SET_NULL, null=True)
    page_realm = models.PositiveSmallIntegerField(default=0)
