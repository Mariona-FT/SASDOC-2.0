from django.shortcuts import render
from .utils import get_sectorchief_section

# Create your views here.

def section_courses_list(request):
    pass

def check_sector_chief_section(request):
    user = request.user
    section,year = get_sectorchief_section(user)  # Call the utility function to fetch the section
    yearselected = request.GET.get('year') or 2024  # Use the default year if no year is selected

    context = {'section': section,'year':year,'yearselected':yearselected}


    return render(request, 'test_sectorchief_info.html', context)