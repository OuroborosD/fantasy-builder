from django.db import models
from character.models import Characters

# Create your models here.
class House(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    members = models.ManyToManyField(Characters, through='Members', related_name='members')
    vassals = models.ManyToManyField(Characters, through='Vassals' )
    house_vassal = models.ManyToManyField('self',  through='VassalHouse')
    def __str__(self):
        return f'{self.name} |  '
#BOOK escrever sobre o erro de mesmo nome
#https://stackoverflow.com/questions/13918968/multiple-many-to-many-relations-to-the-same-model-in-django
class VassalHouse(models.Model):
    fk_house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='vassalhouse_fk_house')
    fk_vassal = models.ForeignKey(House, on_delete=models.CASCADE)
    page = models.SmallIntegerField()


class Members(models.Model):
    fk_house= models.ForeignKey(House, on_delete=models.CASCADE , related_name='member_fk_house')
    fk_character = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name='member_fk_character' )
    page = models.SmallIntegerField()
    def __str__(self):
        return f'{self.fk_character} | {self.fk_house}  '

class Vassals(models.Model):
    fk_house= models.ForeignKey(House, on_delete=models.CASCADE, related_name='vassal_fk_house')
    fk_character = models.ForeignKey(Characters, on_delete=models.CASCADE)
    page = models.SmallIntegerField()
