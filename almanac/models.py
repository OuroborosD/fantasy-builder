from django.db import models

from helper.models import Books, ItemType, Rarity



# Create your models here.
class Almanac(models.Model):
    fk_book = models.ForeignKey(Books, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    rarity = models.ForeignKey(Rarity, on_delete=models.SET_NULL, null= True)
    type = models.ForeignKey(ItemType, on_delete=models.SET_NULL, null= True)
    description = models.TextField()
    value = models.FloatField()
