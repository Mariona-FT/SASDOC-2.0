
from django.shortcuts import render,redirect
from .utils import get_sectionchief_section
from AcademicInfoApp.models import Course,Degree,Year
from ProfSectionCapacityApp.models import CourseYear,TypePoints
from .models import Assigment
from django.urls import reverse

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
        request.session['selected_year'] = year  #global variable selected year in the session
    else:
        year = request.session.get('selected_year', None)
        if not year and years:
            year = years.first().Year  #recent one


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
        
        info_total_course_points= ""  
        info_assigned_points= ""  

        #Return info of TOTAL POINTS - that will need to be assigned that Course year
        for i, point_name in enumerate(typepoint_names):
            point_field = f'Points{chr(65 + i)}'  # PointsA, PointsB..
            point_value = getattr(course_year, point_field, None)
            points[point_name] = point_value if point_value is not None else 0  
            total_course_points += points[point_name]  
            
            info_total_course_points += f"{point_name}: {points[point_name]}, " #better for listing

        info_total_course_points = info_total_course_points.strip(', ')

        #Return info of INFO POINTS ALREADY ASSIGNED x professor that Course year
        assigned_points = {point_name: 0 for point_name in typepoint_names}
        assignments = Assigment.objects.filter(CourseYear=course_year)  
        for assignment in assignments:
            for i, point_name in enumerate(typepoint_names):
                point_field = f'Points{chr(65 + i)}'  # PointsA, PointsB..
                assigned_point_value = getattr(assignment, point_field, None)
                if assigned_point_value is not None:
                    assigned_points[point_name] += assigned_point_value
                    total_assigned_points += assigned_point_value 
        
        for point_name, assigned_value in assigned_points.items():
            info_assigned_points += f"{point_name}: {assigned_value}, " #listing

        info_assigned_points = info_assigned_points.strip(', ')

        #INFO X COURSE
        course_data.append({
            'degree': course_year.Course.Degree.NameDegree,
            'course': course_year.Course.NameCourse,
            'semester': course_year.Semester,
            'year':course_year.Year,

            'total_course_points': total_course_points,
            'total_assigned_points': total_assigned_points,
                        
            'info_total_course_points': info_total_course_points, 
            'info_assigned_points': info_assigned_points, 
        })

    context = {
        'course_data': course_data, 
        'section': section,
        'year': year,
    }   
    return render(request, 'section_courses_assign/courses_assign_list_actions.html', context)
