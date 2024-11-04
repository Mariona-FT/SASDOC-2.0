from django.contrib import admin
from .models import Capacity,Free,CapacitySection,TypePoints
# Register your models here.

class CapacityAdmin(admin.ModelAdmin):
    list_display=["idCapacity","Professor","Year","Points","Comment"]

admin.site.register(Capacity,CapacityAdmin)

class FreeAdmin(admin.ModelAdmin):
    list_display=["idFree","Professor","Year","PointsFree"]

admin.site.register(Free,FreeAdmin)

class CapacitySectionAdmin(admin.ModelAdmin):
    list_display=["idCapacitySection","Professor","Year","Section","Points"]

admin.site.register(CapacitySection,CapacitySectionAdmin)

class TypePointsAdmin(admin.ModelAdmin):
    list_display=["idTypePoints","Year","Section","NamePointsA","NamePointsB","NamePointsC","NamePointsD","NamePointsE"]

admin.site.register(TypePoints,TypePointsAdmin)