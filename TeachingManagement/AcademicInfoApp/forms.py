from django import forms
from .models import Field,Section

class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ['NameField', 'Description', 'isActive']

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['NameSection', 'isActive']