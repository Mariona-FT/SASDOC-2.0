from django import forms
from .models import Field,Section,School,Degree,Course,TypeProfessor,Language,Year
from django.core.exceptions import ValidationError

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
        fields = ['NameSection', 'LetterSection','isActive']
        labels = {
            'NameSection': 'Nom de la Secció',
            'LetterSection':'Lletra de la Secció',
            'isActive': 'És Actiu?',
        }
        widgets = {
            'NameSection': forms.TextInput(attrs={'required': 'required','class': 'form-control'}),
            'LetterSection': forms.TextInput(attrs={'required': 'required','class': 'form-control'}),
            'isActive': forms.CheckboxInput(attrs={'class': 'form-check-input checkbox-field'}),
        }

        help_texts = {
            'LetterSection':'Una o dues lletres pel referir-se a la Secció.',
            'isActive': 'Marqueu si la Secció està actualment activa.',
        }

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['NameSchool', 'CodeSchool','Section','isActive']
        labels = {
            'NameSchool': "Nom de l'Escola",
            'CodeSchool': "Codi de l'Escola",
            'Section': 'Secció',
            'isActive': 'És Actiu?',
        }
        widgets = {
            'NameSchool': forms.TextInput(attrs={'required': 'required','class': 'form-control'}),
            'CodeSchool': forms.NumberInput(attrs={'required': 'required','class': 'form-control'}), 
            'Section':forms.Select(attrs={'class': 'form-select'}),
            'isActive': forms.CheckboxInput(attrs={'class': 'form-check-input checkbox-field'}),
        }
        help_texts = {
            'CodeSchool':"Entra un codi únic per identificar l'Escola.",
            'isActive': "Marqueu si l'Escola està actualment activa.",
        }

class DegreeForm(forms.ModelForm):
    class Meta:
        model = Degree
        fields = ['NameDegree','CodeDegree','School','isActive']
        labels = {
            'NameDegree': 'Nom de la titulació',
            'CodeDegree': 'Codi de la titulació',
            'School': 'Escola',
            'isActive': 'És Actiu?',
        }
        widgets = {
            'NameDegree': forms.TextInput(attrs={'required': 'required','class': 'form-control'}),
            'CodeDegree': forms.NumberInput(attrs={'required': 'required','class': 'form-control'}), 
            'School':forms.Select(attrs={'required': 'required','class': 'form-select'}),
            'isActive': forms.CheckboxInput(attrs={'class': 'form-check-input checkbox-field'}),
        }
        help_texts = {
            'CodeDegree':"Entra un codi únic per identificar la Titulació.",
            'isActive': "Marqueu si la Titulació  està actualment activa.",
        }

    def clean(self):
        cleaned_data = super().clean()
        NameDegree = cleaned_data.get('NameDegree')
        School = cleaned_data.get('School')

        # Check if a Chief already exists with the same professor, year, and section
        if Degree.objects.filter(NameDegree=NameDegree, School=School).exists():
            raise ValidationError('Aquesta Titulació ja existeix en aquesta Escola.')

        return cleaned_data

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['NameCourse', 'CodeCourse', 'ECTS', 'Degree', 'Field', 'isActive']
        labels = {
            'NameCourse': 'Nom del Curs',
            'CodeCourse': 'Codi del Curs',
            'ECTS': 'ECTS',
            'Degree': 'Grau',
            'Field': 'Camp',
            'isActive': 'És Actiu?',
        }

class TypeProfessorForm(forms.ModelForm):
    class Meta:
        model = TypeProfessor
        fields = ['NameContract', 'isFullTime', 'isPermanent', 'Comment', 'isActive']
        labels = {
            'NameContract': 'Tipus del Professor',
            'isFullTime': 'És a Temps Complet?',
            'isPermanent': 'És Permanent?',
            'Comment': 'Comentari',
            'isActive': 'És Actiu?',
        }

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['Language']
        labels = {
            'Language': 'Idioma',
        }

class YearForm(forms.ModelForm):
    class Meta:
        model = Year
        fields = ['Year', 'isEditable']
        labels = {
            'Year': 'Any',
            'isEditable': 'És editable?',
        }
        widgets = {
        'Year': forms.TextInput(attrs={'class': 'form-control',}),
        'isEditable': forms.CheckboxInput(attrs={'class': 'form-check-input checkbox-field'}),
        }
        help_texts = {
            'isEditable': 'Marqueu si aquest any pot ser modificat per un Cap de Secció.',
        }