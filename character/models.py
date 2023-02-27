from django.db import models
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.


class Characters(models.Model):
    name = models.CharField(max_length=50)
    alias = models.CharField(max_length=50, default='N/A')
    birth_year = models.SmallIntegerField()
    season = models.CharField(max_length=30)
    periode = models.CharField(max_length=15)
    slug = models.SlugField(default='', blank=True, null=True, db_index=True)

    def save(self, *args, **kwargs):  # sobrescreve o save metod
        self.slug = slugify(f'{self.name} {self.alias} {self.pk}')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}  {self.alias}'

    def get_absolute_url(self):
        return reverse('character-page', kwargs={'slug': self.slug})


class Proficience(models.Model):
    weapon = models.CharField(max_length=20)
    rank = models.CharField(max_length=20)
    level = models.SmallIntegerField()
    page = models.SmallIntegerField()
    page = models.SmallIntegerField()
    fk_character = models.ForeignKey(Characters, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.fk_character}'


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
