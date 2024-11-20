from django import forms
from .models import Capacity, Free, CapacitySection,TypePoints,CourseYear
from UsersApp.models import Professor
from AcademicInfoApp.models import Year,Section


class CapacityForm(forms.ModelForm):
    class Meta:
        model = Capacity
        fields = ['Professor', 'Year', 'Points', 'Comment']
        labels = {
            'Professor':'Professor',
            'Year':'Any',            
            'Points': 'Punts totals de Capacitat',
            'Comment':'Comentari',
        }
        widgets = {
            'Professor': forms.Select(attrs={'required': 'required','class': 'form-select'}),
            'Year': forms.Select(attrs={'required': 'required','class': 'form-select'}),
            'Points': forms.NumberInput(attrs={'required': 'required','class': 'form-control'}), 
            'Comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Comentari opcional'}),
        }
        help_texts = {
            'Points': "Els punts de capacitat total del Professor aquell any.",
        }

    def __init__(self, *args, **kwargs):
        professor = kwargs.pop('professor', None)
        super().__init__(*args, **kwargs)

        # Dynamically set the queryset for the 'Year' field
        self.fields['Year'].queryset = Year.objects.all().order_by('-Year')

        if professor:
            # If a professor is passed, set it as initial and make it read-only
            self.fields['Professor'].initial = professor
            self.fields['Professor'].disabled = True
        elif self.instance and self.instance.pk:
            # If editing an existing Capacity, make the professor read-only
            self.fields['Professor'].disabled = True


    
class FreeForm(forms.ModelForm):
    class Meta:
        model = Free
        fields = ['Professor', 'Year', 'PointsFree', 'Comment']
        labels = {
            'Professor':'Professor',
            'Year':'Any',
            'Comment':'Comentari',
            'PointsFree': 'Punts lliures',
        }
        widgets = {
            'Professor': forms.Select(attrs={'required': 'required','class': 'form-select'}),
            'Year': forms.Select(attrs={'required': 'required','class': 'form-select'}),
            'PointsFree': forms.NumberInput(attrs={'required': 'required','class': 'form-control'}), 
            'Comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Comentari opcional'}),
        }
        help_texts = {
            'PointsFree': "Els punts que se li poden alliberar al professor aquest any.",
        }
       
    
    def __init__(self, *args, **kwargs):
        professor = kwargs.pop('professor', None)
        super().__init__(*args, **kwargs)
        
        self.fields['Year'].queryset = Year.objects.all().order_by('-Year')

        if professor:
            # If a professor is passed, set it as initial and make it read-only
            self.fields['Professor'].initial = professor
            self.fields['Professor'].disabled = True
        elif self.instance and self.instance.pk:
            # If editing an existing Capacity, make the professor read-only
            self.fields['Professor'].disabled = True
        


class CapacitySectionForm(forms.ModelForm):
    class Meta:
        model = CapacitySection
        fields = ['Professor', 'Year', 'Section', 'Points', 'Comment']
        labels = {
            'Professor':'Professor',
            'Year':'Any',
            'Section':'Secció',
            'Comment':'Comentari',
            'Points': 'Punts totals en la Secció',
        }
        widgets = {
            'Professor': forms.Select(attrs={'required': 'required','class': 'form-select'}),
            'Year': forms.Select(attrs={'required': 'required','class': 'form-select'}),
            'Section': forms.Select(attrs={'required': 'required','class': 'form-select'}),
            'Points': forms.NumberInput(attrs={'required': 'required','class': 'form-control'}), 
            'Comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Comentari opcional'}),
        }  
        help_texts = {
            'Points': "Repartiment dels punts entre les diferent seccions que treballa el professor aquest any.",
        }
       
    
    def __init__(self, *args, **kwargs):
        professor = kwargs.pop('professor', None)
        super().__init__(*args, **kwargs)
        
        self.fields['Year'].queryset = Year.objects.all().order_by('-Year')

        if professor:
            # If a professor is passed, set it as initial and make it read-only
            self.fields['Professor'].initial = professor
            self.fields['Professor'].disabled = True
        elif self.instance and self.instance.pk:
            # If editing an existing Capacity, make the professor read-only
            self.fields['Professor'].disabled = True

class TypePointsForm(forms.ModelForm):
    class Meta:
        model = TypePoints
        fields = ['Year','Section','NamePointsA','NamePointsB','NamePointsC','NamePointsD','NamePointsE']
        labels = {
            'Year':'Any',
            'Section':'Secció',
            'NamePointsA':'Nom pel Tipus de Punts A',
            'NamePointsB':'Nom pel Tipus de Punts B',
            'NamePointsC':'Nom pel Tipus de Punts C',
            'NamePointsD':'Nom pel Tipus de Punts D',
            'NamePointsE':'Nom pel Tipus de Punts E',
        }
        widgets = {
            'NamePointsA': forms.TextInput(attrs={'placeholder': 'Nom Punts A'}),
            'NamePointsB': forms.TextInput(attrs={'placeholder': 'Nom Punts B'}),
            'NamePointsC': forms.TextInput(attrs={'placeholder': 'Nom Punts C'}),
            'NamePointsD': forms.TextInput(attrs={'placeholder': 'Nom Punts D'}),
            'NamePointsE': forms.TextInput(attrs={'placeholder': 'Nom Punts E'}),
        }

    def __init__(self, *args, **kwargs):
        super(TypePointsForm, self).__init__(*args, **kwargs)
        self.fields['Year'].queryset = Year.objects.all().order_by('-Year')  # Order by -Year

class CourseYearForm(forms.ModelForm):
    class Meta:
        model = CourseYear
        fields = [ 'Course', 'Year', 'Semester', 'PointsA', 'PointsB', 'PointsC', 'PointsD', 'PointsE', 'Language']
        labels = {
            'Course': 'Curs',
            'Year': 'Any',
            'Semester': 'Semestre',
            'PointsA': 'Punts A',
            'PointsB': 'Punts B',
            'PointsC': 'Punts C',
            'PointsD': 'Punts D',
            'PointsE': 'Punts E',
            'Language': 'Idioma',
        }

    def __init__(self, *args, **kwargs):
        course = kwargs.pop('Course', None)
        super().__init__(*args, **kwargs)
        
        if course:
            self.fields['Course'].initial = course
            self.fields['Course'].disabled = True  # Makes the field read-only
    
        self.fields['Year'].queryset = Year.objects.all().order_by('-Year')
