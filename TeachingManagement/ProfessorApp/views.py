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
from django.http import HttpResponse
from django.template.loader import render_to_string
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

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
        selected_year = Year.objects.get(pk=selected_year_id)
        selected_year_id = int(selected_year_id) if selected_year_id else 0
        
    except (ValueError, Year.DoesNotExist):
        selected_year = Year.objects.order_by('-Year').first()
        selected_year_id = selected_year.idYear if selected_year else None
    
    if not selected_year:
        messages.error(request, "No hi ha cursos acadèmics disponibles.")
        return render(request, 'info_assignments_professor.html', {'available_years': available_years})
    
   
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
   

    professor_data.append({
        'capacities': capacities,
        'frees': frees,
        'capacity_sections': capacity_sections,
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

        points_summary = get_assigned_points_summary(course_year, professor)

        sections_info[section_name].append({
            'school': course_year.Course.Degree.School.NameSchool,
            'degree': course_year.Course.Degree.NameDegree,
            'course': course_year.Course.NameCourse,
            'semester': course_year.Semester,
            'total_points': total_points,
            'points_summary':points_summary,
            'coordinator': coordinator,
            'coworkers': coworkers,
        })

        
    context = {
        'professor':professor,
        'available_years': available_years,
        'selected_year': selected_year,

        'professor_data': professor_data,        
        'sections_info': sections_info,

    }

    return render(request, 'info_assignments_professor.html',context)

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



def generate_infoassigments_pdf(request):
        # Fetch your data for the template
    data = {
        'title': 'Example PDF',
        'message': 'This is a PDF generated using xhtml2pdf in Django.',
    }

    # Render the HTML template into a string
    html = render_to_string('pdf_template.html', data)

    # Create an HttpResponse object with PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="example.pdf"'

    # Create a PDF using xhtml2pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response
    )

    # Check for errors
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response