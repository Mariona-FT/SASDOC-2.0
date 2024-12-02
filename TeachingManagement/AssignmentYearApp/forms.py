from django import forms
from ProfSectionCapacityApp.models import CourseYear

class CourseYearCommentForm(forms.ModelForm):
    class Meta:
        model = CourseYear
        fields = ['Comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control auto-save', 'rows': 2, 'data-id': '{{ course_year.idCourseYear }}'}),
        }