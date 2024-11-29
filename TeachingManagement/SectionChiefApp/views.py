from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.contrib import messages
from AcademicInfoApp.models import Year
from django.urls import reverse

# Create your views here.

def is_section_chief(user):
    return user.role == 'section_chief'

@login_required
@user_passes_test(is_section_chief)
def section_chief_dashboard(request):
    
    # get SELECTED YEAR - if not selected have the most recent one
    years = Year.objects.all().order_by('-Year').distinct()
    selected_year = request.GET.get('year', None)
    
    if selected_year:
        request.session['selected_year'] = selected_year
    else:
        selected_year = request.session.get('selected_year', None)  #global variable selected year saved in the session
        if not selected_year and years:
            selected_year = years.first().Year #most recent one
    
    context = {'available_years': years, 'selected_year': selected_year,}

    return render(request, 'sectionchief_dashboard.html', context)

""" View to update the selected year in the session."""
def select_year(request):
    if 'year' in request.GET:
        request.session['selected_year'] = request.GET['year']
    
    # Redirect to the page that submitted the form or reload the current page
    referer_url = request.META.get('HTTP_REFERER')
    
    if referer_url:
        return redirect(referer_url)
    else:
        return redirect(reverse('sectionchiefapp:sectionchief_dashboard'))