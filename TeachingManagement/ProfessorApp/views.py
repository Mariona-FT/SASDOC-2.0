from django.shortcuts import render
from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from ProfSectionCapacityApp.models import Professor, Capacity, Free, CapacitySection,TypePoints,CourseYear
from UsersApp.models import Professor
from AcademicInfoApp.models import Section,Year
from AssignmentYearApp.models import Assignment
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
    selected_year == Year.objects.order_by('-Year').first()
   
    user = request.user
    professor=None
    try:
        professor = Professor.objects.get(user=user)
    except Professor.DoesNotExist:
        messages.error(request, "No es troba el professor per l'usuari actual.")
        return render(request, 'info_assignments_professor.html', {'available_years': available_years})

    professor_data=[]
    # Filter capacity, free, and capacity_section entries by the selected year
    capacities = Capacity.objects.filter(Professor=professor, Year=selected_year).order_by('-Year__Year')
    frees = Free.objects.filter(Professor=professor, Year=selected_year).order_by('-Year__Year')
    capacity_sections = CapacitySection.objects.filter(Professor=professor, Year=selected_year).order_by('-Year__Year')
   
    # Calculate the balance
    capacity_points = sum(c.Points for c in capacities)
    free_points = sum(f.PointsFree for f in frees)
    section_points_sum = sum(s.Points for s in capacity_sections)

    balance = capacity_points - free_points - section_points_sum

    professor_data.append({
        'capacities': capacities,
        'frees': frees,
        'capacity_sections': capacity_sections,
        'capacity_points':capacity_points,
        'free_points': free_points,
        'capacity_sections': capacity_sections,
        'balance':balance,
    })


    #Get ALL COURSES for each SECTION assigned
    assignments = Assignment.objects.filter(
        Professor=professor, 
        CourseYear__Year__idYear=selected_year_id
    ).select_related('CourseYear', 'CourseYear__Course', 'CourseYear__Year', 
                    'CourseYear__Course__Degree', 'CourseYear__Course__Degree__School', 
                    'CourseYear__Course__Degree__School__Section')

    # Prepare sections data with the corresponding points for each section
    sections_info = {}
    for capacity_section in capacity_sections:
        section_name = capacity_section.Section.NameSection
        if section_name not in sections_info:
            sections_info[section_name] = []

    course_years = {assignment.CourseYear for assignment in assignments}
    for course_year in course_years:
        # Filter assignments for this specific CourseYear
        section_assignments = [a for a in assignments if a.CourseYear == course_year]

        # Calculate total points for the section
        total_points = sum(
            (a.PointsA or 0) + (a.PointsB or 0) + (a.PointsC or 0) +
            (a.PointsD or 0) + (a.PointsE or 0) + (a.PointsF or 0)
            for a in section_assignments
        )

        # Get coordinator and coworkers
        coordinator = next((a.Professor for a in section_assignments if a.isCoordinator), "")
        coworkers = [
            a.Professor for a in Assignment.objects.filter(CourseYear=course_year)
        ]

        # Append data to result dictionary            
        section_name = course_year.Course.Degree.School.Section.NameSection
        if section_name not in sections_info:
            sections_info[section_name] = []

        sections_info[section_name].append({
            'school': course_year.Course.Degree.School.NameSchool,
            'degree': course_year.Course.Degree.NameDegree,
            'course': course_year.Course.NameCourse,
            'semester': course_year.Semester,
            'total_points': total_points,
            'coordinator': coordinator,
            'coworkers': coworkers,
        })

    # Sort sections_info2 by section name
    sorted_sections_info = sorted(sections_info, key=lambda x: x[0])  # Sorting by section name

        
    context = {
        'professor':professor,
        'available_years': available_years,
        'selected_year': selected_year,

        'professor_data': professor_data,        
        'sections_info': sections_info,

    }

    return render(request, 'info_assignments_professor.html',context)
