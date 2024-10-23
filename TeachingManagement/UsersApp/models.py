from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission # Customize user model
from django.contrib.auth import get_user_model
from django.utils import timezone
from AcademicInfoApp.models import Year,Section,TypeProfessor,Field,Language
# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('director', 'Director'),
        ('sector_chief', 'Sector Chief'),
        ('professor', 'Professor'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set', 
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions '
                  'granted to each of their groups.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

#PROFESSOR MODEL
class Professor(models.Model):
    #Custom PK
    idProfessor = models.CharField(max_length=10, primary_key=True, unique=True)  

    # ForeignKey to CustomUser
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    # Additional professor-specific fields
    name = models.CharField(max_length=100)
    family_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    email = models.EmailField(unique=True)
    
    ACTIVE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    isActive = models.CharField(max_length=3, choices=ACTIVE_CHOICES, default='yes')
    current_contract = models.ForeignKey(TypeProfessor, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name='professor'
        verbose_name_plural='professors'

    def __str__(self):
        return f"{self.name} {self.family_name}"


# PROFESSOR-FIELD MODEL (Many-to-Many)
class ProfessorField(models.Model):
    idProfessorField = models.AutoField(primary_key=True)
    Professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='professor_fields')
    Field = models.ForeignKey(Field, on_delete=models.CASCADE)
    Comment=models.TextField(null=True,blank=True)

    def __str__(self):
        return f"{self.Professor.name} - {self.Field.NameField}"

# PROFESSOR-LANGUAGE MODEL (Many-to-Many)
class ProfessorLanguage(models.Model):
    idProfessorLanguage = models.AutoField(primary_key=True)
    Professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='professor_languages')
    Language = models.ForeignKey(Language, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.Professor.name} - {self.Language.Language}"
    

#CHIEF MODEL
class Chief(models.Model):
    
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    #year = models.CharField(max_length=4, default=str(timezone.now().year))  # Default is the current year
    year = models.ForeignKey(Year, on_delete=models.SET_NULL, null=True)

    #section = models.CharField(max_length=100)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name='section chief'
        verbose_name_plural='section chiefs'
            

    def __str__(self):
        return f"{self.professor.name} {self.professor.family_name} - {self.section} ({self.year})"