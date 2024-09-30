from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission # Customize user model

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