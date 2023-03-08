from django.contrib import admin
from .models import *
# Register your models here.

class CharacterAdmin(admin.ModelAdmin):
    
    prepopulated_fields = {'slug':('name','alias', 'birth_year', 'season')}

#BOOK refazer a parte de admin com imagens
admin.site.register(Characters,CharacterAdmin)
admin.site.register(Proficience)
admin.site.register(Status)
admin.site.register(Skills)
admin.site.register(CharacterSkills)
admin.site.register(CharacterProficience)
admin.site.register(Realms)