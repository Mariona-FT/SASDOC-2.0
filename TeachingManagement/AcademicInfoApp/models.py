from django.db import models

# Create your models here.

class Field(models.Model):
    idField = models.AutoField(primary_key=True)
    NameField = models.CharField(max_length=100)
    Description = models.TextField()
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.NameField