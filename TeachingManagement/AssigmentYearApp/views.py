
from django.shortcuts import render,redirect
from .utils import get_sectionchief_section

# Create your views here.

def section_courses_list(request):
    pass

def check_section_chief_section(request):
    user = request.user
    section,year = get_sectionchief_section(user)  # Call the utility function to fetch the section

    context = {'section': section,'year':year}


    return render(request, 'test_sectionchief_info.html', context)
