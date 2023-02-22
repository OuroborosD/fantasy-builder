from django.db import models

# Create your models here.
class Characters(models.Model):
    name = models.CharField(max_length=50)
    alias = models.CharField(max_length=50)
    age = models.SmallIntegerField(default=0)
    birth =  models.CharField(max_length=50)


    def __str__(self):
        return f'{self.name} nasceu no {self.birth}'