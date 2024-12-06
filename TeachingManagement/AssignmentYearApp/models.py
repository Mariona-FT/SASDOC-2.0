from django.db import models
from UsersApp.models import Professor
from ProfSectionCapacityApp.models import CourseYear

# Create your models here.

class Assignment(models.Model):
    idAssignment = models.AutoField(primary_key=True)
    CourseYear = models.ForeignKey(CourseYear, on_delete=models.CASCADE)
    Professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    PointsA = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    PointsB = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    PointsC = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    PointsD = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    PointsE = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    PointsF = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    IsCoordinator = models.BooleanField(default=False)

    class Meta:
        verbose_name='assignment'
        verbose_name_plural='assignments'
        unique_together = ('Professor', 'CourseYear')  # Ensure unique combinations


    def __str__(self):
        return f"{self.Professor.name} {self.Professor.family_name} {self.CourseYear.Course.NameCourse}  {self.CourseYear.Year.Year}"

