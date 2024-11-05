from django import forms
from .models import Capacity, Free, CapacitySection
from UsersApp.models import Professor
from AcademicInfoApp.models import Year,Section

class CapacityForm(forms.ModelForm):
    class Meta:
        model = Capacity
        fields = ['Professor', 'Year', 'Points', 'Comment']

class FreeForm(forms.ModelForm):
    class Meta:
        model = Free
        fields = ['Professor', 'Year', 'PointsFree']

class CapacitySectionForm(forms.ModelForm):
    class Meta:
        model = CapacitySection
        fields = ['Professor', 'Year', 'Section', 'Points']


class CapacityFreeSectionForm(forms.Form):
    professor = forms.ModelChoiceField(queryset=Professor.objects.all(), label='Professor')
    year = forms.ModelChoiceField(queryset=Year.objects.all(), label='Year')
    section = forms.ModelChoiceField(queryset=Section.objects.all(), label='Section')
    points = forms.IntegerField(initial=0, label='Capacity Points')
    commentcapacity = forms.CharField(required=False, widget=forms.Textarea, label='Comment capacitat')
    commentfree = forms.CharField(required=False, widget=forms.Textarea, label='Comment hores lliures')
    commentcapacitysection = forms.CharField(required=False, widget=forms.Textarea, label='Comment capacitat secció')
    points_free = forms.IntegerField(initial=0, label='Free Points')
    capacity_section_points = forms.IntegerField(initial=0, label='Capacity Section Points')

    def save(self):
        professor = self.cleaned_data['professor']
        year = self.cleaned_data['year']
        section = self.cleaned_data['section']
        
        points = self.cleaned_data['points']
        commentcapacity = self.cleaned_data['commentcapacity']
        
        points_free = self.cleaned_data['points_free']
        commentfree = self.cleaned_data['commentfree']
        
        capacity_section_points = self.cleaned_data['capacity_section_points']
        commentcapacitysection=self.cleaned_data['commentcapacitysection']

        # Create Capacity
        # Handle Capacity - unique for Professor-Year
        capacity, created = Capacity.objects.update_or_create(
            Professor=professor,
            Year=year,
            defaults={'Points': points, 'Comment': commentcapacity}
        )


        # Handle Free - unique for Professor-Year
        free, created = Free.objects.update_or_create(
            Professor=professor,
            Year=year,
            defaults={'PointsFree': points_free,'Comment':commentfree}
        )


        # Create CapacitySection
        capacity_section, created = CapacitySection.objects.update_or_create(
            Professor=professor,
            Year=year,
            Section=section,
            defaults={'Points': capacity_section_points,'Comment':commentcapacitysection}
        )


        return capacity, free, capacity_section