from django import forms
from .models import Field,Section,School

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