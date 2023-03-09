from django.contrib import admin
from .models import Kingdom, Region, Settlement, Fief,Local

# Register your models here.


admin.site.register(Kingdom)
admin.site.register(Region)
admin.site.register(Settlement)
admin.site.register(Fief)
admin.site.register(Local)