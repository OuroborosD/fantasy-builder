from django.db import models

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
        return f'{self.pk} | {self.rank} '
    

class ItemType(models.Model):
    type = models.CharField(max_length=50)
    description = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return f'{self.type}'


##############################Geography###################################################

class Localization(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return f'{self.name} |  '


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
    
    
##############################Character###################################################



class RelatioshipsType(models.Model):
    name = models.CharField(max_length=30)



######################### time helpers############################3

class Season(models.Model):
    season = models.CharField(max_length=15)
    def __str__(self):
        return f'{self.season}'

class Periode(models.Model):
    periode = models.CharField(max_length=15)
    def __str__(self):
        return f'{self.periode}'
    



