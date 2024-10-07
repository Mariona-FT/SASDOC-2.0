from django import forms
from .models import Field,Section,School,Degree,TypeProfessor,Lenguage

class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ['NameField', 'Description', 'isActive']
        labels = {
            'NameField': "Nom del Camp",
            'Description': 'Descripció',
            'isActive': 'És Actiu?',
        }

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['NameSection', 'isActive']
        labels = {
            'NameSection': 'Nom de la Secció',
            'isActive': 'És Actiu?',
        }

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['NameSchool', 'Section','isActive']
        labels = {
            'NameSchool': "Nom de l'Escola",
            'Section': 'Secció',
            'isActive': 'És Actiu?',
        }

class DegreeForm(forms.ModelForm):
    class Meta:
        model = Degree
        fields = ['NameDegree', 'School','isActive']
        labels = {
            'NameDegree': 'Nom del Grau',
            'School': 'Escola',
            'isActive': 'És Actiu?',
        }

class TypeProfessorForm(forms.ModelForm):
    class Meta:
        model = TypeProfessor
        fields = ['Name', 'isFullTime', 'isPermanent', 'Comment', 'isActive']
        labels = {
            'Name': 'Tipus del Professor',
            'isFullTime': 'És a Temps Complet?',
            'isPermanent': 'És Permanent?',
            'Comment': 'Comentari',
            'isActive': 'És Actiu?',
        }

class LenguageForm(forms.ModelForm):
    class Meta:
        model = Lenguage
        fields = ['Lenguage']
        labels = {
            'Lenguage': 'Llenguatge',
        }