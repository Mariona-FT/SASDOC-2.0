from django.shortcuts import render
from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from ProfSectionCapacityApp.models import Professor, Capacity, Free, CapacitySection,TypePoints,CourseYear
from UsersApp.models import Professor,ProfessorField,ProfessorLanguage
from AcademicInfoApp.models import Section,Year
from AssignmentYearApp.models import Assignment
from django.contrib import messages
from itertools import chain
from django.db.models import Sum
from django.http import HttpResponse
from django.template.loader import render_to_string
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from decimal import Decimal

# Create your views here

def is_professor(user):
    return user.role == 'professor'

@login_required
@user_passes_test(is_professor)
def professor_dashboard(request):
    professor = get_object_or_404(Professor, user=request.user)

 # Get professor's languages and fields
    languages = ProfessorLanguage.objects.filter(Professor=professor)
    fields = ProfessorField.objects.filter(Professor=professor)

    # If no languages or fields are found, set them to an empty string
    languages_list = ', '.join([language.Language.Language for language in languages]) if languages else "Encara no assignats."
    fields_list = ', '.join([field.Field.NameField for field in fields]) if fields else "Encara no assignats."

    context = {
        'professor': professor,
        'languages_list': languages_list,
        'fields_list': fields_list,
    }

    return render(request, 'professor_dashboard.html',context)

def get_professor_assignments_data(request):
    available_years = Year.objects.all().order_by('-Year').distinct()
    selected_year_id = request.GET.get('year')
    selected_year = None

    try:
        selected_year = Year.objects.get(pk=selected_year_id)
    except (ValueError, Year.DoesNotExist):
        selected_year = Year.objects.order_by('-Year').first()

    if not selected_year:
        return None, {"error": "No hi ha cursos acadèmics disponibles."}

    user = request.user
    try:
        professor = Professor.objects.get(user=user)
    except Professor.DoesNotExist:
        return None, {"error": "No es troba el professor per l'usuari actual."}

    professor_data = []
    capacities = Capacity.objects.filter(Professor=professor, Year=selected_year).order_by('-Year__Year')
    frees = Free.objects.filter(Professor=professor, Year=selected_year).order_by('-Year__Year')
    capacity_sections = CapacitySection.objects.filter(Professor=professor, Year=selected_year).order_by('-Year__Year')

    capacity_data = []
    for capacity in capacities:
        total_points = capacity.Points or 0
        total_hours = total_points * Decimal(3.3333)
        capacity_data.append({
            'object': capacity,
            'total_hours': total_hours,
        })
    
    free_data = []
    for free in frees:
        total_points = free.PointsFree or 0 
        total_hours = total_points * Decimal(3.3333)
        free_data.append({
            'object': free,
            'total_hours': total_hours,
        })

    capacity_section_data = []
    for cap_section in capacity_sections:
        total_points = cap_section.Points or 0  
        total_hours = total_points * Decimal(3.3333)
        capacity_section_data.append({
            'object':cap_section,
            'total_hours': total_hours,
        })

    professor_data.append({
        'capacities': capacity_data,
        'frees': free_data,
        'capacity_sections': capacity_section_data,
    })

    assignments = Assignment.objects.filter(
        Professor=professor, 
        CourseYear__Year__idYear=selected_year.idYear
    ).select_related(
        'CourseYear', 'CourseYear__Course', 'CourseYear__Year', 
        'CourseYear__Course__Degree', 'CourseYear__Course__Degree__School', 
        'CourseYear__Course__Degree__School__Section'
    )

    sections_info = {}
    for capacity_section in capacity_sections:
        section_name = capacity_section.Section.NameSection
        if section_name not in sections_info:
            sections_info[section_name] = []

    course_years = {assignment.CourseYear for assignment in assignments}
    for course_year in course_years:
        section_assignments = [a for a in assignments if a.CourseYear == course_year]
        total_points = sum(
            (a.PointsA or 0) + (a.PointsB or 0) + (a.PointsC or 0) +
            (a.PointsD or 0) + (a.PointsE or 0) + (a.PointsF or 0)
            for a in section_assignments
        )
        coordinator = next((a.Professor for a in section_assignments if a.isCoordinator), "")
        coworkers = [
        {
            'name': a.Professor.name,
            'family_name': a.Professor.family_name,
            'total_points':(
                (a.PointsA or 0) + (a.PointsB or 0) + (a.PointsC or 0) +
                (a.PointsD or 0) + (a.PointsE or 0) + (a.PointsF or 0)
            ),
            'total_hours': (
                ((a.PointsA or 0) + (a.PointsB or 0) + (a.PointsC or 0) +
                (a.PointsD or 0) + (a.PointsE or 0) + (a.PointsF or 0)) * Decimal(3.3333)
            )
        }
        for a in Assignment.objects.filter(CourseYear=course_year)
        ]

        section_name = course_year.Course.Degree.School.Section.NameSection
        if section_name not in sections_info:
            sections_info[section_name] = []

        points_summary = get_assigned_points_summary(course_year, professor)
        sections_info[section_name].append({
            'school': course_year.Course.Degree.School.NameSchool,
            'degree': course_year.Course.Degree.NameDegree,
            'course': course_year.Course.NameCourse,
            'semester': course_year.Semester,
            'total_points': total_points,
            'total_hours': (total_points * Decimal(3.3333)),
            'points_summary': points_summary,
            'coordinator': coordinator,
            'coworkers': coworkers,
        })

    return {
        'professor': professor,
        'available_years': available_years,
        'selected_year': selected_year,
        'professor_data': professor_data,
        'sections_info': sections_info,
    }, None

#return the string with the points and the typepoints for each courseyear 
def get_assigned_points_summary(courseyear,professor):
    section=courseyear.Course.Degree.School.Section
    year=courseyear.Year
    typepoints_section = TypePoints.objects.filter(Section=section, Year=year).first()

    # Extract the names of point types dynamically
    typepoint_names_assigned = {}
    if typepoints_section:
        typepoints_fields = {
            'PointsA': 'NamePointsA',
            'PointsB': 'NamePointsB',
            'PointsC': 'NamePointsC',
            'PointsD': 'NamePointsD',
            'PointsE': 'NamePointsE',
            'PointsF': 'NamePointsF',
        }
        for field, name_field in typepoints_fields.items():
            point_name = getattr(typepoints_section, name_field, None)
            if point_name: 
                typepoint_names_assigned[field] = point_name

    assigned_points = {name: 0 for name in typepoint_names_assigned.values()}

    assignments = Assignment.objects.filter(CourseYear=courseyear,Professor=professor)

    for assignment in assignments:
        for field, point_name in typepoint_names_assigned.items():
            assigned_value = getattr(assignment, field, 0) or 0
            assigned_points[point_name] += assigned_value

    points_summary = ", ".join([f"{point_name}: {value}" for point_name, value in assigned_points.items()])
    
    return points_summary

#given a professor or section chief entered by LOGIN - visualizing its information
@login_required
def info_assignments(request):
    context, error = get_professor_assignments_data(request)
    if error:
        messages.error(request, error['error'])
        return render(request, 'info_assignments_professor.html', {'available_years': context.get('available_years', [])})

    return render(request, 'info_assignments_professor.html', context)

#same function as get_assigned_points_summary, but given a PROFESSOR and YEAR - to see more information 
def get_professor_year_assignments_data(professor_id, year_id):
    available_years = Year.objects.all().order_by('-Year').distinct()

    selected_year = get_object_or_404(Year, pk=year_id)
    professor = get_object_or_404(Professor, pk=professor_id)

    # Fetch data similar to the original function
    professor_data = []
    capacities = Capacity.objects.filter(Professor=professor, Year=selected_year).order_by('-Year__Year')
    frees = Free.objects.filter(Professor=professor, Year=selected_year).order_by('-Year__Year')
    capacity_sections = CapacitySection.objects.filter(Professor=professor, Year=selected_year).order_by('-Year__Year')

    capacity_data = []
    for capacity in capacities:
        total_points = capacity.Points or 0
        total_hours = total_points * Decimal(3.3333)
        capacity_data.append({
            'object': capacity,
            'total_hours': total_hours,
        })
    
    free_data = []
    for free in frees:
        total_points = free.PointsFree or 0 
        total_hours = total_points * Decimal(3.3333)
        free_data.append({
            'object': free,
            'total_hours': total_hours,
        })

    capacity_section_data = []
    for cap_section in capacity_sections:
        total_points = cap_section.Points or 0  
        total_hours = total_points * Decimal(3.3333)
        capacity_section_data.append({
            'object': cap_section,
            'total_hours': total_hours,
        })

    professor_data.append({
        'capacities': capacity_data,
        'frees': free_data,
        'capacity_sections': capacity_section_data,
    })

    assignments = Assignment.objects.filter(
        Professor=professor, 
        CourseYear__Year__idYear=selected_year.idYear
    ).select_related(
        'CourseYear', 'CourseYear__Course', 'CourseYear__Year', 
        'CourseYear__Course__Degree', 'CourseYear__Course__Degree__School', 
        'CourseYear__Course__Degree__School__Section'
    )

    sections_info = {}
    for capacity_section in capacity_sections:
        section_name = capacity_section.Section.NameSection
        if section_name not in sections_info:
            sections_info[section_name] = []

    course_years = {assignment.CourseYear for assignment in assignments}
    for course_year in course_years:
        section_assignments = [a for a in assignments if a.CourseYear == course_year]
        total_points = sum(
            (a.PointsA or 0) + (a.PointsB or 0) + (a.PointsC or 0) +
            (a.PointsD or 0) + (a.PointsE or 0) + (a.PointsF or 0)
            for a in section_assignments
        )
        coordinator = next((a.Professor for a in section_assignments if a.isCoordinator), "")
        coworkers = [
        {
            'name': a.Professor.name,
            'family_name': a.Professor.family_name,
            'total_points':(
                (a.PointsA or 0) + (a.PointsB or 0) + (a.PointsC or 0) +
                (a.PointsD or 0) + (a.PointsE or 0) + (a.PointsF or 0)
            ),
            'total_hours': (
                ((a.PointsA or 0) + (a.PointsB or 0) + (a.PointsC or 0) +
                (a.PointsD or 0) + (a.PointsE or 0) + (a.PointsF or 0)) * Decimal(3.3333)
            )
        }
        for a in Assignment.objects.filter(CourseYear=course_year)
        ]

        section_name = course_year.Course.Degree.School.Section.NameSection
        if section_name not in sections_info:
            sections_info[section_name] = []

        points_summary = get_assigned_points_summary(course_year, professor)
        sections_info[section_name].append({
            'school': course_year.Course.Degree.School.NameSchool,
            'degree': course_year.Course.Degree.NameDegree,
            'course': course_year.Course.NameCourse,
            'semester': course_year.Semester,
            'total_points': total_points,
            'total_hours': (total_points * Decimal(3.3333)),
            'points_summary': points_summary,
            'coordinator': coordinator,
            'coworkers': coworkers,
        })

    return {
        'professor': professor,
        'available_years': available_years,
        'selected_year': selected_year,
        'professor_data': professor_data,
        'sections_info': sections_info,
    }

#given a professor or sector chief for SEEING ITS DETAILS
@login_required
def professor_year_assignments_summary(request, professor_id, year_id):
    data = get_professor_year_assignments_data(professor_id, year_id)
    if isinstance(data, dict):  # Valid data
        return render(request, 'details_professor_assignments.html', data)
    else:
        return render(request, 'details_professor_assignments.html', {'error': data.get('error')})


@login_required
def generate_assignments_pdf(request):
    
    selected_year_id = request.GET.get('year')
    selected_year = None
    if selected_year_id:
        try:
            selected_year = Year.objects.get(pk=selected_year_id)
        except Year.DoesNotExist:
            selected_year = None
    
    if not selected_year:
        # If no year is selected, use the most recent year
        selected_year = Year.objects.order_by('-Year').first()

    context, error = get_professor_assignments_data(request)
    if error:
        messages.error(request, error['error'])
        return render(request, 'info_assignments_professor.html', {'available_years': context.get('available_years', [])})

    render(request, 'info_assignments_professor.html', context)

    user = request.user
    try:
        professor = Professor.objects.get(user=user)
    except Professor.DoesNotExist:
        return None, {"error": "No es troba el professor per l'usuari actual."}


    professor_name = f"{professor.name}_{professor.family_name}".replace(" ", "_")
    year_label = selected_year.Year if selected_year else "sense_any"

    filename = f"assignacio_docent_{professor_name}_{year_label}.pdf"
   
    # Generate HTML from template
    html = render_to_string('pdf_template.html', context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Errors occurred while generating PDF:<pre>' + html + '</pre>')

    return response

#Given de PROFESSOR and YEAR to see its details
@login_required
def generate_professor_year_assignments_pdf(request, professor_id, year_id):
    professor = get_object_or_404(Professor, pk=professor_id)
    selected_year = get_object_or_404(Year, pk=year_id)

    # Fetch the data related to the professor and year
    data = get_professor_year_assignments_data(professor_id, year_id)

    if not data:
        messages.error(request, "No data found for the selected professor and year.")
        return HttpResponse('No data found.')

    professor_name = f"{professor.name}_{professor.family_name}".replace(" ", "_")
    year_label = selected_year.Year if selected_year else "no_year"
    filename = f"assignacio_docent_{professor_name}_{year_label}.pdf"

    # Generate the HTML from template
    html = render_to_string('pdf_template.html', data)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error occurred while generating the PDF.')

    return response