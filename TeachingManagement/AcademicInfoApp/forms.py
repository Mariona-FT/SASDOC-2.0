from django import forms
from .models import Field,Section,School,Degree,Course,TypeProfessor,Language,Year
from django.core.exceptions import ValidationError

class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ['NameField', 'Description', 'isActive']
        labels = {
            'NameField': "Nom",
            'Description': 'Descripció',
            'isActive': 'És actiu?',
        }
        widgets = {
            'NameField': forms.TextInput(attrs={'required': 'required','class': 'form-control'}),
            'Description': forms.Textarea(attrs={'rows': 3,'class': 'form-control'}),
            'isActive': forms.CheckboxInput(attrs={'class': 'form-check-input checkbox-field'}),
        }

        help_texts = {
            'Description': 'Opcional.',
            'isActive': 'Marcar si el camp de coneixament està actiu.',
        }

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['NameSection', 'LetterSection','isActive']
        labels = {
            'NameSection': 'Nom',
            'LetterSection':'Acrònim',
            'isActive': 'És activa?',
        }
        widgets = {
            'NameSection': forms.TextInput(attrs={'required': 'required','class': 'form-control'}),
            'LetterSection': forms.TextInput(attrs={'required': 'required','class': 'form-control'}),
            'isActive': forms.CheckboxInput(attrs={'class': 'form-check-input checkbox-field'}),
        }

        help_texts = {
            'LetterSection':'Màxim de 5 lletres.',
            'isActive': 'Marcar si la secció està activa.',
        }

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['NameSchool', 'CodeSchool','Section','isActive']
        labels = {
            'NameSchool': "Nom",
            'CodeSchool': "Codi",
            'Section': 'Secció',
            'isActive': 'És activa?',
        }
        widgets = {
            'NameSchool': forms.TextInput(attrs={'required': 'required','class': 'form-control'}),
            'CodeSchool': forms.NumberInput(attrs={'required': 'required','class': 'form-control'}), 
            'Section':forms.Select(attrs={'class': 'form-select'}),
            'isActive': forms.CheckboxInput(attrs={'class': 'form-check-input checkbox-field'}),
        }
        help_texts = {
            'CodeSchool':"Entra un codi únic.",
            'isActive': "Marcar si l'escola està activa.",
        }

class DegreeForm(forms.ModelForm):
    class Meta:
        model = Degree
        fields = ['NameDegree','CodeDegree','School','isActive']
        labels = {
            'NameDegree': 'Nom ',
            'CodeDegree': 'Codi',
            'School': 'Escola',
            'isActive': 'És actiu?',
        }
        widgets = {
            'NameDegree': forms.TextInput(attrs={'required': 'required','class': 'form-control'}),
            'CodeDegree': forms.NumberInput(attrs={'required': 'required','class': 'form-control'}), 
            'School':forms.Select(attrs={'required': 'required','class': 'form-select'}),
            'isActive': forms.CheckboxInput(attrs={'class': 'form-check-input checkbox-field'}),
        }
        help_texts = {
            'CodeDegree':"Entra un codi únic.",
            'isActive': "Marcar si la titulació està activa.",
        }

    def clean(self):
        cleaned_data = super().clean()
        name_degree = cleaned_data.get('NameDegree')
        school = cleaned_data.get('School')

        instance = self.instance  # The current instance of Degree being edited

        if instance.pk:
            # Exclude the current instance from the query to allow for editing the same object
            if Degree.objects.filter(NameDegree=name_degree, School=school).exclude(pk=instance.pk).exists():
                raise ValidationError('Aquesta titulació ja existeix en aquesta escola.')

        else:
            # Check if a Degree already exists with the same NameDegree and School (for new entries)
            if Degree.objects.filter(NameDegree=name_degree, School=school).exists():
                raise ValidationError('Aquesta titulació ja existeix en aquesta escola.')


        return cleaned_data

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['NameCourse', 'CodeCourse', 'ECTS', 'Degree', 'Field', 'isActive']
        labels = {
            'NameCourse': 'Nom',
            'CodeCourse': 'Codi',
            'ECTS': 'ECTS',
            'Degree': 'Titulació',
            'Field': 'Camp de coneixament',
            'isActive': 'És actiu?',
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
            'CodeCourse':"Entra un codi únic.",
            'isActive': "Marcar l'assignatura està activa.",
        }

    def clean(self):
        cleaned_data = super().clean()
        code_course = cleaned_data.get('CodeCourse')
        degree = cleaned_data.get('Degree')

        instance = self.instance  # The current instance of Course being edited

        if instance.pk:
            # Exclude the current instance from the query to allow for editing the same object
            if Course.objects.filter(CodeCourse=code_course, Degree=degree).exclude(pk=instance.pk).exists():
                raise ValidationError('Aquesta assignatura ja existeix en aquesta titulació.')

        else:
            # Check if a Course already exists with the same CodeCourse and Degree (for new entries)
            if Course.objects.filter(CodeCourse=code_course, Degree=degree).exists():
                raise ValidationError('Aquesta assignatura ja existeix en aquesta titulació.')

        return cleaned_data

class TypeProfessorForm(forms.ModelForm):
    class Meta:
        model = TypeProfessor
        fields = ['NameContract', 'isFullTime', 'isPermanent', 'Comment', 'isActive']
        labels = {
            'NameContract': 'Tipus de contracte',
            'isFullTime': 'És a temps complet?',
            'isPermanent': 'És permanent?',
            'Comment': 'Comentari',
            'isActive': 'És actiu?',
        }
        widgets = {
            'NameContract': forms.TextInput(attrs={'required': 'required','class': 'form-control'}),
            'isFullTime': forms.CheckboxInput(attrs={'class': 'form-check-input checkbox-field'}),
            'isPermanent': forms.CheckboxInput(attrs={'class': 'form-check-input checkbox-field'}),
            'Comment': forms.Textarea(attrs={'rows': 3,'class': 'form-control'}),
            'isActive': forms.CheckboxInput(attrs={'class': 'form-check-input checkbox-field'}),
        }
        help_texts = {
            'Comment':"Opcional.",
            'isActive': "Marcar si el contracte està actiu.",
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
                raise ValidationError('Ja existeix un contracte amb aquest nom, a temps complet i permanent.')

        else:
            # Check if a TypeProfessor already exists with the same NameContract, isFullTime, and isPermanent (for new entries)
            if TypeProfessor.objects.filter(NameContract=name_contract, isFullTime=is_full_time, isPermanent=is_permanent).exists():
                raise ValidationError('Ja existeix un contracte amb aquest nom, a temps complet i permanent.')
        return cleaned_data

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['Language']
        labels = {
            'Language': 'Idioma',
        }
        widgets = {
            'Language': forms.TextInput(attrs={'required': 'required','class': 'form-control',}),
        }

class YearForm(forms.ModelForm):
    class Meta:
        model = Year
        fields = ['Year', 'isEditable']
        labels = {
            'Year': "Curs acadèmic",
            'isEditable': 'És editable?',
        }
        widgets = {
            'Year': forms.TextInput(attrs={'required': 'required','class': 'form-control',}),
            'isEditable': forms.CheckboxInput(attrs={'class': 'form-check-input checkbox-field'}),
        }
        help_texts = {
            'isEditable': "Si les dades poden ser modificades per un cap de secció.",
        }