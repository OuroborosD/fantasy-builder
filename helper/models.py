import datetime
from django.db import models
from django.utils.text import slugify
from datetime import datetime


# Create your models here.

##############################Murim###################################################
class WeaponsType(models.Model):
    weapon = models.CharField(max_length=25)
    description = models.TextField()
    
    def __str__(self):
        return f'{self.weapon} {self.pk}'
    

class SkillMastery(models.Model):
    rank = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return f'{self.rank} '
    

class ItemType(models.Model):
    type = models.CharField(max_length=50)
    description = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return f'{self.type}'


##############################Geography###################################################

class Localization(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return f'{self.name}'


class Economy(models.Model):
    name = models.CharField(max_length=50)
    descrition = models.TextField()
    def __str__(self):
        return f'{self.name}'


class CountryType(models.Model):
    name =  models.CharField(max_length=50)
    description = models.TextField()
    def __str__(self):
        return f'{self.name} '
    

class SettlementType(models.Model):
    name =  models.CharField(max_length=50)
    description = models.TextField()
    def __str__(self):
        return f'{self.name} '


class Resource(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    def __str__(self):
        return f'{self.name}'
    
##############################Character###################################################



class RelatioshipsType(models.Model):
    name = models.CharField(max_length=30)



######################### time helpers ############################3

class Season(models.Model):
    season = models.CharField(max_length=15)
    def __str__(self):
        return f'{self.season}'

class Periode(models.Model):
    periode = models.CharField(max_length=15)
    def __str__(self):
        return f'{self.periode}'


###################### book ##################################

class BookColection(models.Model):
    name = models.CharField(max_length=50)



class Books(models.Model):
    title = models.CharField(max_length=80)
    subtitle = models.CharField(max_length=80)
    is_colection = models.BooleanField(default=False)
    type = models.CharField(max_length=30, choices=(('murim','murim'),('fantasy','fantasy'),))
    colection = models.ForeignKey(BookColection, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(unique=True, default='', blank=True, null=True, db_index=True)

    
    def save(self, *args, **kwargs):  # sobrescreve o save metod
        time =  datetime.now()
        t = time.strftime("%M%S")
        self.slug = slugify(
            f'{self.title} {t} {self.subtitle} ')
        super().save(*args, **kwargs)


