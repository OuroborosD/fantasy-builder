
from django.db import models
from django.utils.text import slugify
from datetime import datetime

from helper.models import Books, Economy, Localization, CountryType, Resource

# Create your models here.


class Country(models.Model):
    fk_book = models.ForeignKey(Books, on_delete=models.SET_NULL, null= True)
    name = models.CharField(max_length=50)
    rank = models.ForeignKey(CountryType, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(unique=True, default='', blank=True, null=True, db_index=True)

    def save(self, *args, **kwargs):  # sobrescreve o save metod
        time =  datetime.now()
        t = time.strftime("%M%S")
        self.slug = slugify(
            f'{self.name}  {self.rank} {t}')
        super().save(*args, **kwargs)
      


    def __str__(self):
        return f'{self.name}  |{self.slug} '


class Region(models.Model):
    name = models.CharField(max_length=50)
    localization = models.ManyToManyField(Localization)
    description = models.TextField()
    fk_country = models.ForeignKey(Country, on_delete=models.CASCADE)
    slug = models.SlugField(default='', blank=True, null=True, db_index=True)

    def save(self, *args, **kwargs):  # sobrescreve o save metod
        print(f'12	linha -------arquivo: {self.slug}------- valor:	')
        time =  datetime.now()
        t = time.strftime("%M%S")
        self.slug = slugify(
            f'{self.name} {t}')
        super(Region, self).save()

    def __str__(self):
            return f'fk:{self.fk_country} {self.name}'


class Fief(models.Model):
    name = models.CharField(max_length=50)
    localization = models.ManyToManyField(Localization)
    size = models.SmallIntegerField(blank=True, null=True)
    description = models.TextField()
    fk_region = models.ForeignKey(Region, on_delete=models.CASCADE)
    slug = models.SlugField(default='', blank=True, null=True, db_index=True)

    def save(self, *args, **kwargs):  # sobrescreve o save metod
        
        time =  datetime.now()
        t = time.strftime("%M%S")
        self.slug = slugify(
            f'{self.name} {t} ')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


class Settlement(models.Model):
    name = models.CharField(max_length=50)
    localization = models.ManyToManyField(Localization)
    type = models.CharField(max_length=20)  # town, city village etc
    population = models.PositiveIntegerField(blank=True, null=True)
    economy = models.ManyToManyField(Economy)
    description = models.TextField()
    slug = models.SlugField(default='', blank=True, null=True, db_index=True)
    fk_fief= models.ForeignKey(Fief, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):  # sobrescreve o save metod
        time =  datetime.now()
        t = time.strftime("%M%S")
        self.slug = slugify(
            f'{self.name}   {t}')
        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.name}'





class Local(models.Model):
    name = models.CharField(max_length=50)
    localization = models.ManyToManyField(Localization)
    resource = models.ManyToManyField(Resource, blank=True)
    description = models.TextField(default='N/A')
    fk_settlement = models.ForeignKey(
        Settlement, on_delete=models.CASCADE, null=True)
    fk_fief = models.ForeignKey(Fief, on_delete=models.CASCADE, null=True)
    fk_region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)
    fk_country = models.ForeignKey(
        Country, on_delete=models.CASCADE, null=True)
