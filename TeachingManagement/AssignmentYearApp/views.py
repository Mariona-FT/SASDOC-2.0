
from django.shortcuts import render,redirect,get_object_or_404
from .utils import get_sectionchief_section
from AcademicInfoApp.models import Course,Degree,Year
from ProfSectionCapacityApp.models import CourseYear,TypePoints
from .models import Assignment
from django.urls import reverse
from django.http import JsonResponse
import json
from django.contrib import messages

# Create your views here.

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
    
#Testing
def check_section_chief_section(request):
    user = request.user
    section,year = get_sectionchief_section(user)  # Call the utility function to fetch the section

    context = {'section': section,'year':year}
    return render(request, 'test_sectionchief_info.html', context)

# COURSES found in that SECTION - IN ALL SCHOOLS - IN ALL DEGREES
def section_courses_list(request):
    user=request.user
    section,year= get_sectionchief_section(user) # return the section of the chief

    # get SELECTED YEAR - if not selected have the most recent one
    years = Year.objects.all().order_by('-Year').distinct()
    year = request.GET.get('year', None)
    
    if year:
        request.session['selected_year'] = year  #global variable selected year saved in the session
    else:
        year = request.session.get('selected_year', None)
        if not year and years:
            year = years.first().Year  #most recent one


    year_obj = Year.objects.get(Year=year)

    #return COURSES associated with the section, year, and schools/degrees
    course_years  = CourseYear.objects.filter(
        Course__Degree__School__Section=section, 
        Year=year_obj.idYear
    ).select_related('Course', 'Year', 'Course__Degree')

    #return NAMES of the TYPE of POINTS
    typepoints_section=TypePoints.objects.filter(
        Section=section, 
        Year=year_obj.idYear 
    ).first()

    #extract the NAMES OF TYPE POINTS of that section - only save the not empty names 
    typepoint_names = []
    if typepoints_section:
        typepoint_fields = ['NamePointsA', 'NamePointsB', 'NamePointsC', 'NamePointsD', 'NamePointsE', 'NamePointsF']
        for field in typepoint_fields:
            point_name = getattr(typepoints_section, field)
            if point_name:  
                typepoint_names.append(point_name)

    course_data = [] #all info of ONE COURSE
   
    for course_year in course_years:
        points = {}
        total_course_points = 0         #total points TO assign in the course - initial points
        total_assigned_points = 0       #total ALREADY assigned points - where professors wil be assigned

        #Return info of TOTAL POINTS - that will need to be assigned that Course year
        for i, point_name in enumerate(typepoint_names):
            point_field = f'Points{chr(65 + i)}'  # PointsA, PointsB..
            point_value = getattr(course_year, point_field, None)
            points[point_name] = point_value if point_value is not None else 0  
            
            total_course_points += points[point_name]  
        
        #Return info of INFO POINTS ALREADY ASSIGNED x professor that Course year
        assigned_points = {point_name: 0 for point_name in typepoint_names}
       
        assignments = Assignment.objects.filter(CourseYear=course_year)  
        for assignment in assignments:
            for i, point_name in enumerate(typepoint_names):
                point_field = f'Points{chr(65 + i)}'  # PointsA, PointsB..
                assigned_point_value = getattr(assignment, point_field, None)
                if assigned_point_value is not None:
                    assigned_points[point_name] += assigned_point_value
                    total_assigned_points += assigned_point_value 
        
        # Create formatted string for each point type in "Group: assigned/total" format
        points_summary = ""
        for point_name in typepoint_names:
            assigned_value = assigned_points.get(point_name, 0)
            total_value = points.get(point_name, 0)
            points_summary += f"{point_name}: {assigned_value}/{total_value} , "

        # Remove the trailing comma and space
        points_summary = points_summary.strip(', ')

        #INFO X COURSE
        course_data.append({
            'id':course_year.idCourseYear,
            'degree': course_year.Course.Degree.NameDegree,
            'course': course_year.Course.NameCourse,
            'semester': course_year.Semester,
            'year':course_year.Year,

            'total_course_points': total_course_points,
            'total_assigned_points': total_assigned_points,
                        
            'points_summary':points_summary,
        })

    context = {
        'course_data': course_data, 
        'section': section,
    }   
    return render(request, 'section_courses_assign/courses_assign_list_actions.html', context)

def courseyear_show(request,idCourseYear=None):
    course_year = get_object_or_404(CourseYear, pk=idCourseYear)

     # Return NAMES of the TYPE of POINTS for the course's section and year
    typepoints_section = TypePoints.objects.filter(
        Section=course_year.Course.Section,
        Year=course_year.Year
    ).first()

    #extract the NAMES OF TYPE POINTS of that section - only save the not empty names 
    typepoint_names = []
    if typepoints_section:
        typepoint_fields = ['NamePointsA', 'NamePointsB', 'NamePointsC', 'NamePointsD', 'NamePointsE', 'NamePointsF']
        for field in typepoint_fields:
            point_name = getattr(typepoints_section, field)
            if point_name:  
                typepoint_names.append(point_name)

    # Retrieve total points from CourseYear and assigned points from Assignment
    total_points = {}
    assigned_points = {name: 0 for name in typepoint_names}

    for i, point_name in enumerate(typepoint_names):
        point_field = f'Points{chr(65 + i)}'  # PointsA, PointsB, etc.
        total_points[point_name] = getattr(course_year, point_field, 0) or 0

    # Retrieve assignments and calculate assigned points
    assignments = Assignment.objects.filter(CourseYear=course_year)
    for assignment in assignments:
        for i, point_name in enumerate(typepoint_names):
            point_field = f'Points{chr(65 + i)}'  # PointsA, PointsB, etc.
            assigned_value = getattr(assignment, point_field, 0)
            if assigned_value is not None:
                assigned_points[point_name] += assigned_value

    context = {
        'course_year': course_year,
        'typepoint_names': typepoint_names,
        'total_points': total_points,
        'assigned_points': assigned_points,
    }

    # Pass the course_year data to the template
    return render(request, 'section_courses_assign/overview_course_assign.html', {'course_year': course_year})

def update_course_year_comment(request,idCourseYear):
    course_year = get_object_or_404(CourseYear, pk=idCourseYear)

    if request.method == 'POST':
        comment = request.POST.get('comment', '').strip()
        
        if comment:
            course_year.Comment = comment
            course_year.save()
            messages.success(request, f"El comentari s'ha actualitzat correctament.")
        else:
            messages.error(request, 'El comentari no és vàlid. Si us plau, escriu un comentari.')
        return render(request, 'section_courses_assign/overview_course_assign.html', {'course_year': course_year})


    messages.error(request, f"El comentari no sha creat correctament.")
    return render(request, 'section_courses_assign/overview_course_assign.html', {'course_year': course_year})

