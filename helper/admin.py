from django.contrib import admin
from helper.models import WeaponsType, SkillMastery, Localization, Economy, CountryType, Season,Periode
# Register your models here.

admin.site.register(WeaponsType)
admin.site.register(SkillMastery)
admin.site.register(Economy)
admin.site.register(Localization)
admin.site.register(CountryType)
admin.site.register(Season)
admin.site.register(Periode)
