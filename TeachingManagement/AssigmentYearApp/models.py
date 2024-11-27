from django.db import models
from UsersApp.models import Professor
from ProfSectionCapacityApp.models import CourseYear

# Create your models here.

class Assigment(models.Model):
    idAssigment = models.AutoField(primary_key=True)
    CourseYear = models.ForeignKey(CourseYear, on_delete=models.CASCADE)
    Professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    PointsA = models.IntegerField(null=True, blank=True)
    PointsB = models.IntegerField(null=True, blank=True)
    PointsC = models.IntegerField(null=True, blank=True)
    PointsD = models.IntegerField(null=True, blank=True)
    PointsE = models.IntegerField(null=True, blank=True)
    PointsF = models.IntegerField(null=True, blank=True)
    IsCoordinator = models.BooleanField(default=False)

    class Meta:
        verbose_name='assigment'
        verbose_name_plural='assigments'
        unique_together = ('Professor', 'CourseYear')  # Ensure unique combinations


    def __str__(self):
        return f"{self.Professor.name} {self.Professor.family_name} {self.CourseYear.Course.NameCourse}  {self.CourseYear.Year.Year}"

