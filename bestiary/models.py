from django.db import models
from django.utils.text import slugify
from datetime import datetime


from helper.models import Books
from murim.models import  Realms





# Create your models here.
class MagicBeast(models.Model):
    fk_book = models.ForeignKey(Books, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    img = models.ImageField(upload_to='images/beast/%Y/%m/%d/', default='images/default/bestiary.jpeg')
    murim_realm = models.ForeignKey(Realms, on_delete=models.SET_NULL, null=True)
    fantasy_atribute = models.PositiveSmallIntegerField(null=True)
    description = models.TextField()
    slug = models.SlugField(unique=True, default='', blank=True, null=True, db_index=True)

    def save(self, *args, **kwargs):  # sobrescreve o save metod
        if self.slug == '':
            time =  datetime.now()
            t = time.strftime("%M%S")
            self.slug = slugify(
                f'{self.name}  {self.fk_book.pk} {t}')
        super().save(*args, **kwargs)


class Loot(models.Model):
    fk_book = models.ForeignKey(Books, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(default='N/A')
    value = models.FloatField(default=0)
    def __str__(self):
        return f'{self.name}'

class MagicBeastLoot(models.Model):
    fk_beast = models.ForeignKey(MagicBeast, on_delete= models.CASCADE)
    fk_loot = models.ForeignKey(Loot, on_delete= models.CASCADE)
    qtd_meter = models.PositiveSmallIntegerField(null=True, blank=True)
    qtd_kg = models.PositiveIntegerField(null=True, blank=True)
