from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

# Create your views here.

def is_section_chief(user):
    return user.role == 'sector_chief'

@login_required
@user_passes_test(is_section_chief)
def section_chief_dashboard(request):
    return render(request, 'sectionchief_dashboard.html')