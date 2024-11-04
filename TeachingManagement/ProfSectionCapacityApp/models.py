from django.db import models
from AcademicInfoApp.models import Year,Section
from UsersApp.models import Professor

# Create your models here.

class Capacity(models.Model):
    idCapacity = models.AutoField(primary_key=True)
    Professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    Year = models.ForeignKey(Year, on_delete=models.CASCADE)
    Points = models.IntegerField(default=0)
    Comment = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name='capacity'
        verbose_name_plural='capacitys'

    def __str__(self):
        return f"{self.Professor.name} {self.Professor.family_name} - {self.Year.Year} - Points: {self.Points}"


class Free(models.Model):
    idFree = models.AutoField(primary_key=True)
    Professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    Year = models.ForeignKey(Year, on_delete=models.CASCADE)
    PointsFree = models.IntegerField(default=0)

    class Meta:
        verbose_name='free'
        verbose_name_plural='frees'

    def __str__(self):
        return f"{self.Professor.name} {self.Professor.family_name} - {self.Year.Year} - Free Points: {self.PointsFree}"


class CapacitySection(models.Model):
    idCapacitySection = models.AutoField(primary_key=True)
    Professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    Year = models.ForeignKey(Year, on_delete=models.CASCADE)
    Section = models.ForeignKey(Section, on_delete=models.CASCADE)
    Points = models.IntegerField(default=0)

    class Meta:
        verbose_name='capacitysection'
        verbose_name_plural='capacitysections'

    def __str__(self):
        return f"{self.Professor.name} {self.Professor.family_name} - {self.Year.Year} - {self.Section.NameSection} - Points: {self.Points}"


class TypePoints(models.Model):
    idTypePoints = models.AutoField(primary_key=True)
    Year = models.ForeignKey(Year, on_delete=models.CASCADE)
    Section = models.ForeignKey(Section, on_delete=models.CASCADE)
    NamePointsA = models.CharField(max_length=100,default=0)
    NamePointsB = models.CharField(max_length=100,default=0)
    NamePointsC = models.CharField(max_length=100,default=0)
    NamePointsD = models.CharField(max_length=100,default=0)
    NamePointsE = models.CharField(max_length=100,default=0)

    class Meta:
        verbose_name='typepoints'
        verbose_name_plural='typepoints'

    def __str__(self):
        return f"{self.Year.Year} - {self.Section.NameSection}"