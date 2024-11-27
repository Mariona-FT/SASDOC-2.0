# In context_processors.py
from AcademicInfoApp.models import Year

def global_years(request):
    selected_year = request.session.get('selected_year', None)
    
    if not selected_year:
        selected_year = Year.objects.first().Year if Year.objects.exists() else None

    years = Year.objects.all().order_by('-Year').distinct()
    
    return {
        'global_available_years': years,  # List of all years
        'global_selected_year': selected_year  # The currently selected year (from session or default)
    }