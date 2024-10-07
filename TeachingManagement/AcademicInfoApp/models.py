from django.db import models

# Create your models here.

class Field(models.Model):
    idField = models.AutoField(primary_key=True)
    NameField = models.CharField(max_length=100)
    Description = models.TextField()
    isActive = models.BooleanField(default=True)

    class Meta:
        verbose_name='field'
        verbose_name_plural='fields'
            
    def __str__(self):
        return self.NameField
    
class Section(models.Model):
    idSection = models.AutoField(primary_key=True)
    NameSection = models.CharField(max_length=100)
    isActive = models.BooleanField(default=True)

    class Meta:
        verbose_name='section'
        verbose_name_plural='sections'

    def __str__(self):
        return self.NameSection

class School(models.Model):
    idSchool = models.AutoField(primary_key=True)
    NameSchool = models.CharField(max_length=100)
    Section = models.ForeignKey('Section', on_delete=models.SET_NULL, null=True) #do not eliminate schools if section eliminated
    isActive = models.BooleanField(default=True)

    class Meta:
        verbose_name='school'
        verbose_name_plural='schools'

    def __str__(self):
        return self.NameSchool

class Degree(models.Model):
    idDegree = models.AutoField(primary_key=True)
    NameDegree = models.CharField(max_length=100)
    School = models.ForeignKey('School', on_delete=models.SET_NULL, null=True) #do not eliminate degree if school eliminated
    isActive = models.BooleanField(default=True)

    class Meta:
        verbose_name='degree'
        verbose_name_plural='degrees'

    def __str__(self):
        return self.NameDegree
    
class Courses(models.Model):
    idCourse = models.AutoField(primary_key=True)
    NameCourse = models.CharField(max_length=100)
    CodeCourse = models.IntegerField()
    ECTS = models.IntegerField()
    Degree = models.ForeignKey('Degree', on_delete=models.CASCADE, null=True) #eliminate course if degree eliminated
    Field = models.ForeignKey('Field', on_delete=models.SET_NULL, null=True) #do not course if field eliminated
    isActive = models.BooleanField(default=True)

    class Meta:
        verbose_name='course'
        verbose_name_plural='courses'

    def __str__(self):
        return f"{self.NameCourse} ({self.Degree})"
    
class TypeProfessor(models.Model):
    idTypeProfessor = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    isFullTime = models.BooleanField(default=False)
    isPermanent = models.BooleanField(default=False)
    Comment = models.TextField(blank=True, null=True)
    isActive = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'type of professor'
        verbose_name_plural = 'types of professors'

    def __str__(self):
        return self.Name

class Lenguage(models.Model):
    idLenguage = models.AutoField(primary_key=True)
    Lenguage = models.CharField(max_length=20,unique=True)

    class Meta:
        verbose_name='lenguage'
        verbose_name_plural='lenguages'

    def __str__(self):
        return self.Lenguage

class Year(models.Model):
    Year = models.IntegerField(primary_key=True,unique=True)
    isActive = models.BooleanField(default=False)

    class Meta:
        verbose_name='year'
        verbose_name_plural='years'

    def __str__(self):
        return str(self.Year)