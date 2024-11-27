from django.contrib import admin
from .models import Assigment

# Register your models here.

class AssigmentAdmin(admin.ModelAdmin):
    list_display=["idAssigment","CourseYear","Professor","IsCoordinator","PointsA","PointsB","PointsC","PointsD","PointsE","PointsF"]

admin.site.register(Assigment,AssigmentAdmin)