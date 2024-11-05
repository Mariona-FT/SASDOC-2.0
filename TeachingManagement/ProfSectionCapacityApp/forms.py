from django import forms
from .models import Capacity, Free, CapacitySection
from UsersApp.models import Professor
from AcademicInfoApp.models import Year,Section


class CapacityForm(forms.ModelForm):
    class Meta:
        model = Capacity
        fields = ['Professor', 'Year', 'Points', 'Comment']
        widgets = {
            'Comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional comment'}),
        }
        labels = {
            'Points': 'Total Capacity Points',
        }

    def __init__(self, *args, **kwargs):
        professor = kwargs.pop('professor', None)
        super().__init__(*args, **kwargs)
        
        if professor:
            self.fields['Professor'].initial = professor
            self.fields['Professor'].disabled = True  # Makes the field read-only
    
class FreeForm(forms.ModelForm):
    class Meta:
        model = Free
        fields = ['Professor', 'Year', 'PointsFree', 'Comment']
        widgets = {
            'Comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional comment'}),
        }
        labels = {
            'PointsFree': 'Free Capacity Points',
        }

class CapacitySectionForm(forms.ModelForm):
    class Meta:
        model = CapacitySection
        fields = ['Professor', 'Year', 'Section', 'Points', 'Comment']
        widgets = {
            'Comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional comment'}),
        }
        labels = {
            'Points': 'Section Capacity Points',
        }