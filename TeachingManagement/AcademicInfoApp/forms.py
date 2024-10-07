from django import forms
from .models import Field,Section,School,Degree

class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ['NameField', 'Description', 'isActive']

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['NameSection', 'isActive']

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['NameSchool', 'Section','isActive']

class DegreeForm(forms.ModelForm):
    class Meta:
        model = Degree
        fields = ['NameDegree', 'School','isActive']