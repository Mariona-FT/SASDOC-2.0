from django.shortcuts import render
from .utils import get_sectionchief_section

# Create your views here.

def section_courses_list(request):
    pass

def check_section_chief_section(request):
    user = request.user
    section,year = get_sectionchief_section(user)  # Call the utility function to fetch the section
    yearselected = request.GET.get('year') or 2024  # Use the default year if no year is selected

    context = {'section': section,'year':year,'yearselected':yearselected}


    return render(request, 'test_sectionchief_info.html', context)