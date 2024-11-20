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
        widgets = {
            'NameField': forms.TextInput(attrs={'required': 'required','class': 'form-control'}),
            'Description': forms.Textarea(attrs={'rows': 3,'class': 'form-control'}),
            'isActive': forms.CheckboxInput(attrs={'class': 'form-check-input checkbox-field'}),
        }

        help_texts = {
            'Description': 'Descripció del Camp és opcional.',
            'isActive': 'Marqueu si el Camp està actualment actiu.',
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
            'isActive': "Marqueu si la Titulació està actualment activa.",
        }

    def clean(self):
        cleaned_data = super().clean()
        name_degree = cleaned_data.get('NameDegree')
        school = cleaned_data.get('School')

        instance = self.instance  # The current instance of Degree being edited

        if instance.pk:
            # Exclude the current instance from the query to allow for editing the same object
            if Degree.objects.filter(NameDegree=name_degree, School=school).exclude(pk=instance.pk).exists():
                raise ValidationError('Aquesta Titulació ja existeix en aquesta Escola.')

        else:
            # Check if a Degree already exists with the same NameDegree and School (for new entries)
            if Degree.objects.filter(NameDegree=name_degree, School=school).exists():
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
        widgets = {
            'NameCourse': forms.TextInput(attrs={'required': 'required','class': 'form-control'}),
            'CodeCourse': forms.NumberInput(attrs={'required': 'required','class': 'form-control'}), 
            'ECTS': forms.TextInput(attrs={'required': 'required','class': 'form-control'}),
            'Degree':forms.Select(attrs={'required': 'required','class': 'form-select'}),
            'Field':forms.Select(attrs={'required': 'required','class': 'form-select'}),
            'isActive': forms.CheckboxInput(attrs={'class': 'form-check-input checkbox-field'}),
        }
        help_texts = {
            'CodeCourse':"Entra un codi únic per identificar el Curs.",
            'isActive': "Marqueu si el Curs està actualment actiu.",
        }

    def clean(self):
        cleaned_data = super().clean()
        code_course = cleaned_data.get('CodeCourse')
        degree = cleaned_data.get('Degree')

        instance = self.instance  # The current instance of Course being edited

        if instance.pk:
            # Exclude the current instance from the query to allow for editing the same object
            if Course.objects.filter(CodeCourse=code_course, Degree=degree).exclude(pk=instance.pk).exists():
                raise ValidationError('Aquest Curs ja existeix en aquesta Titulació.')

        else:
            # Check if a Course already exists with the same CodeCourse and Degree (for new entries)
            if Course.objects.filter(CodeCourse=code_course, Degree=degree).exists():
                raise ValidationError('Aquest Curs ja existeix en aquesta Titulació.')

        return cleaned_data

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
        widgets = {
            'NameContract': forms.TextInput(attrs={'required': 'required','class': 'form-control'}),
            'isFullTime': forms.CheckboxInput(attrs={'class': 'form-check-input checkbox-field'}),
            'isPermanent': forms.CheckboxInput(attrs={'class': 'form-check-input checkbox-field'}),
            'Comment': forms.Textarea(attrs={'rows': 3,'class': 'form-control'}),
            'isActive': forms.CheckboxInput(attrs={'class': 'form-check-input checkbox-field'}),
        }
        help_texts = {
            'isFullTime':"Marqueu si el Tipus de professor és a Temps Complet.",
            'isPermanent':"Marqueu si el Tipus de professor és Permanent.",
            'Comment':"Comentari Opcional.",
            'isActive': "Marqueu si el Curs està actualment actiu.",
        }

    def clean(self):
        cleaned_data = super().clean()
        name_contract = cleaned_data.get('NameContract')
        is_full_time = cleaned_data.get('isFullTime')
        is_permanent = cleaned_data.get('isPermanent')

        instance = self.instance  # The current instance of TypeProfessor being edited

        if instance.pk:
            # Exclude the current instance from the query to allow for editing the same object
            if TypeProfessor.objects.filter(NameContract=name_contract, isFullTime=is_full_time, isPermanent=is_permanent).exclude(pk=instance.pk).exists():
                raise ValidationError('Ja existeix un tipus de professorat amb aquest nom, a temps complet i permanent.')

        else:
            # Check if a TypeProfessor already exists with the same NameContract, isFullTime, and isPermanent (for new entries)
            if TypeProfessor.objects.filter(NameContract=name_contract, isFullTime=is_full_time, isPermanent=is_permanent).exists():
                raise ValidationError('Ja existeix un tipus de professorat amb aquest nom, a temps complet i permanent.')
        return cleaned_data

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