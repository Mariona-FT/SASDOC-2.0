from django.shortcuts import render
from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from ProfSectionCapacityApp.models import Professor, Capacity, Free, CapacitySection,TypePoints,CourseYear
from UsersApp.models import Professor
from AcademicInfoApp.models import Section,Year
from django.contrib import messages
from itertools import chain
from django.db.models import Sum
# Create your views here

def is_professor(user):
    return user.role == 'professor'

@login_required
@user_passes_test(is_professor)
def professor_dashboard(request):
    return render(request, 'professor_dashboard.html')

@login_required
@user_passes_test(is_professor)
def info_assignments(request):
    available_years = Year.objects.all().order_by('-Year').distinct()
    
    # Selected year ID and object
    selected_year_id = request.GET.get('year')
    selected_year = None

    # Try to retrieve the selected year, default to the most recent year
    try:
        selected_year_id = int(selected_year_id) if selected_year_id else 0
        selected_year = Year.objects.get(pk=selected_year_id)
    except (ValueError, Year.DoesNotExist):
        selected_year = Year.objects.order_by('-Year').first()
        if not selected_year:
            messages.error(request, "No hi ha cursos acadèmics disponibles.")
            return render(request, 'info_assignments_professor.html', {'available_years': available_years})
    
    # Determine if the selected year is the most recent year
    is_most_recent_year = selected_year == Year.objects.order_by('-Year').first()
   
    user = request.user
    professor=None
    try:
        professor = Professor.objects.get(user=user)
    except Professor.DoesNotExist:
        messages.error(request, "No es troba el professor per l'usuari actual.")
        return render(request, 'info_assignments_professor.html', {'available_years': available_years})

    #Capacity - punts totals - of selected year
    capacity = Capacity.objects.filter(Year=selected_year, Professor=professor).first()
    if not capacity:
        total_capacity = 0
    else:
        total_capacity = capacity.Points if hasattr(capacity, 'Points') else 0


    context = {
        'professor':professor,
        'available_years': available_years,
        'selected_year': selected_year,
        'is_most_recent_year': is_most_recent_year,
        'capacity':capacity,
        # 'professor_id': professor_id,
        # 'assignment_data': assignment_data,
    }

    return render(request, 'info_assignments_professor.html',context)
