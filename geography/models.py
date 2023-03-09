from django.db import models
from helper.models import Economy, Localization, CountryType

# Create your models here.
class Kingdom(models.Model):
    name = models.CharField(max_length=50)
    rank = models.SmallIntegerField(choices=CountryType.objects.all().values_list('id','name'))#empire, kingdom, etc
    def __str__(self):
        return f'{self.name} | {self.rank} '

class Region(models.Model):
    name = models.CharField(max_length=50)
    localization = models.ManyToManyField(Localization)
    description = models.TextField()
    fk_kingdom = models.ForeignKey(Kingdom, on_delete=models.CASCADE)

class Fief(models.Model):
    name = models.CharField(max_length=50)
    localization = models.ManyToManyField(Localization)
    size = models.SmallIntegerField()
    description = models.TextField()
    fk_region = models.ForeignKey(Kingdom, on_delete=models.CASCADE)


class Settlement(models.Model):
    name = models.CharField(max_length=50)
    localization = models.ManyToManyField(Localization)
    type = models.CharField(max_length=20) #town, city village etc
    population = models.PositiveIntegerField()
    economy = models.ManyToManyField(Economy)
    description = models.TextField()
    fk_kingdom = models.ForeignKey(Kingdom, on_delete=models.CASCADE)



class Local(models.Model):
    description = models.TextField()
    fk_settlement = models.ForeignKey(Settlement, on_delete=models.CASCADE, null=True)
    fk_fief = models.ForeignKey(Fief, on_delete=models.CASCADE , null=True)
    fk_region = models.ForeignKey(Region, on_delete=models.CASCADE , null=True)
    fk_kingdom = models.ForeignKey(Kingdom, on_delete=models.CASCADE , null=True)