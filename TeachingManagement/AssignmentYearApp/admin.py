from django.contrib import admin
from .models import Assignment

# Register your models here.

class AssignmentAdmin(admin.ModelAdmin):
    list_display=["idAssignment","CourseYear","Professor","isCoordinator","PointsA","PointsB","PointsC","PointsD","PointsE","PointsF"]

admin.site.register(Assignment,AssignmentAdmin)