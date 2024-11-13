from django import forms
from .models import Capacity, Free, CapacitySection,TypePoints
from UsersApp.models import Professor
from AcademicInfoApp.models import Year,Section


class CapacityForm(forms.ModelForm):
    class Meta:
        model = Capacity
        fields = ['Professor', 'Year', 'Points', 'Comment']
        widgets = {
            'Comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Comentari opcional'}),
        }
        labels = {
            'Professor':'Professor',
            'Year':'Any',
            'Comment':'Comentari',
            'Points': 'Punts totals de Capacitat',
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
            'Comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Comentari opcional'}),
        }
        labels = {
            'Professor':'Professor',
            'Year':'Any',
            'Comment':'Comentari',
            'PointsFree': 'Punts lliures',
        }
    
    def __init__(self, *args, **kwargs):
        professor = kwargs.pop('professor', None)
        super().__init__(*args, **kwargs)
        
        if professor:
            self.fields['Professor'].initial = professor
            self.fields['Professor'].disabled = True  # Makes the field read-only

class CapacitySectionForm(forms.ModelForm):
    class Meta:
        model = CapacitySection
        fields = ['Professor', 'Year', 'Section', 'Points', 'Comment']
        widgets = {
            'Comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Comentari opcional'}),
        }
        labels = {
            'Professor':'Professor',
            'Year':'Any',
            'Section':'Secció',
            'Comment':'Comentari',
            'Points': 'Punts totals en la Secció',
        }
    
    def __init__(self, *args, **kwargs):
        professor = kwargs.pop('professor', None)
        super().__init__(*args, **kwargs)
        
        if professor:
            self.fields['Professor'].initial = professor
            self.fields['Professor'].disabled = True  # Makes the field read-only


class TypePointsForm(forms.ModelForm):
    class Meta:
        model = TypePoints
        fields = ['Year','Section','NamePointsA','NamePointsB','NamePointsC','NamePointsD','NamePointsE']
        labels = {
            'Year':'Any',
            'Section':'Secció',
            'NamePointsA':'Nom Tipus Punts A',
            'NamePointsB':'Nom Tipus Punts B',
            'NamePointsC':'Nom Tipus Punts C',
            'NamePointsD':'Nom Tipus Punts D',
            'NamePointsE':'Nom Tipus Punts E',
        }
        widgets = {
            'NamePointsA': forms.TextInput(attrs={'placeholder': 'Nom Tipus Punts A'}),
            'NamePointsB': forms.TextInput(attrs={'placeholder': 'Nom Tipus Punts B'}),
            'NamePointsC': forms.TextInput(attrs={'placeholder': 'Nom Tipus Punts C'}),
            'NamePointsD': forms.TextInput(attrs={'placeholder': 'Nom Tipus Punts D'}),
            'NamePointsE': forms.TextInput(attrs={'placeholder': 'Nom Tipus Punts E'}),
        }
