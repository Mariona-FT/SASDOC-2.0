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
    source_year_id = request.session.get('source_year', None)
    target_year_id = request.session.get('target_year', None)


    source_year = Year.objects.filter(idYear=source_year_id).first() if source_year_id else None
    target_year = Year.objects.filter(idYear=target_year_id).first() if target_year_id else None


    return {
        'source_year': source_year,
        'target_year': target_year,
    }