# In context_processors.py
from AcademicInfoApp.models import Year

def global_years(request):
    global_available_years = Year.objects.all().order_by('-Year')
    global_selected_year = request.session.get('selected_year', global_available_years.first().Year if global_available_years else None)
    
    return {
        'global_available_years': global_available_years,  # List of all years
        'global_selected_year': global_selected_year  # The currently selected year (from session or default)
    }


def selected_years(request):
    source_year = request.session.get('source_year', None)
    target_year = request.session.get('target_year', None)

    return {
        'source_year': source_year,
        'target_year': target_year,
    }