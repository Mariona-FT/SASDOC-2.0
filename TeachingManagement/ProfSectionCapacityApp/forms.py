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


class CombinedForm(forms.Form):
    professor = forms.ModelChoiceField(queryset=Professor.objects.all(), label='Professor')
    year = forms.ModelChoiceField(queryset=Year.objects.all(), label='Year')
    section = forms.ModelChoiceField(queryset=Section.objects.all(), label='Section')
    points = forms.IntegerField(initial=0, label='Capacity Points')
    comment = forms.CharField(required=False, widget=forms.Textarea, label='Comment')
    points_free = forms.IntegerField(initial=0, label='Free Points')
    capacity_section_points = forms.IntegerField(initial=0, label='Capacity Section Points')

    def save(self):
        professor = self.cleaned_data['professor']
        year = self.cleaned_data['year']
        section = self.cleaned_data['section']
        points = self.cleaned_data['points']
        comment = self.cleaned_data['comment']
        points_free = self.cleaned_data['points_free']
        capacity_section_points = self.cleaned_data['capacity_section_points']

        # Create Capacity
        capacity = Capacity.objects.create(
            Professor=professor,
            Year=year,
            Points=points,
            Comment=comment
        )

        # Create Free
        free = Free.objects.create(
            Professor=professor,
            Year=year,
            PointsFree=points_free
        )

        # Create CapacitySection
        capacity_section = CapacitySection.objects.create(
            Professor=professor,
            Year=year,
            Section=section,
            Points=capacity_section_points
        )

        return capacity, free, capacity_section