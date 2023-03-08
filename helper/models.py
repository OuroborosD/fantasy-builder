from django.db import models

# Create your models here.


class WeaponsType(models.Model):
    weapon = models.CharField(max_length=25)
    description = models.TextField()
    
    def __str__(self):
        return f'{self.weapon} {self.pk}'
    



