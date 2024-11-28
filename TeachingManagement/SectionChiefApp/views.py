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
    years = Year.objects.all().order_by('-Year').distinct()

   # Retrieve the selected year from the GET request or fall back to the session
    selected_year = request.GET.get('year', None)
    
    if selected_year:
        # If a new year is selected via GET request, store it in the session
        request.session['selected_year'] = selected_year
    else:
        # If no year is selected in the GET request, use the session value
        selected_year = request.session.get('selected_year', None)
        
        # If there's no year in the session, default to the most recent year from the database
        if not selected_year and years:
            selected_year = years.first().Year  # Or you can choose the most recent year by your own logic

    
    context = {'available_years': years, 'selected_year': selected_year,}

    return render(request, 'sectionchief_dashboard.html', context)


def select_year(request):
    """
    View to update the selected year in the session.
    """
    if 'year' in request.GET:
        request.session['selected_year'] = request.GET['year']
    
    # Redirect to the page that submitted the form or reload the current page
    referer_url = request.META.get('HTTP_REFERER')
    
    if referer_url:
        return redirect(referer_url)
    else:
        return redirect(reverse('sectionchiefapp:sectionchief_dashboard'))