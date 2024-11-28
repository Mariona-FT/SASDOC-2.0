
from django.shortcuts import render,redirect
from .utils import get_sectionchief_section
from AcademicInfoApp.models import Course,Degree,Year
from ProfSectionCapacityApp.models import CourseYear,TypePoints
from .models import Assigment
from django.urls import reverse

# Create your views here.


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
    

def check_section_chief_section(request):
    user = request.user
    section,year = get_sectionchief_section(user)  # Call the utility function to fetch the section

    context = {'section': section,'year':year}


    return render(request, 'test_sectionchief_info.html', context)

# COURSES found in that SECTION - IN ALL SCHOOLS - IN ALL DEGREES
def section_courses_list(request):
    user=request.user
    section,year= get_sectionchief_section(user) # return the section of the chief

    years = Year.objects.all().order_by('-Year').distinct()
    year = request.GET.get('year', None)
    
    if year:
        # If a new year is selected via GET request, store it in the session
        request.session['selected_year'] = year
    else:
        # If no year is selected in the GET request, use the session value
        year = request.session.get('selected_year', None)
        
        # If there's no year in the session, default to the most recent year from the database
        if not year and years:
            year = years.first().Year  # Or you can choose the most recent year by your own logic

    print(f"Selected Year: {year}")  # Debugging line to check the value of year

    year_obj = Year.objects.get(Year=year)

    # Fetch COURSES associated with the section, year, and schools/degrees
    course_years  = CourseYear.objects.filter(
        Course__Degree__School__Section=section,  # Filter by Section
        Year=year_obj.idYear
    ).select_related('Course', 'Year', 'Course__Degree')

    #return NAMES of the TYPE of POINTS
    typepoints_section=TypePoints.objects.filter(
        Section=section,  # Filter by Section
        Year=year_obj.idYear  # Filter by Year
    ).first()

    #extract the NAMES OF TYPE POINTS of that section - only save the not empty names 
    typepoint_names = []
    if typepoints_section:
        typepoint_fields = ['NamePointsA', 'NamePointsB', 'NamePointsC', 'NamePointsD', 'NamePointsE', 'NamePointsF']
        for field in typepoint_fields:
            point_name = getattr(typepoints_section, field)
            if point_name:  # Check if the field is not empty or None
                typepoint_names.append(point_name)

    #extract POINTS for each course and add them to a list of dictionaries
    course_data = [] #all info of ONE COURSE
   
    for course_year in course_years:
        points = {}
        total_course_points = 0         #total points TO assign in the course
        total_assigned_points = 0       #total ALREADY assigned points
        
        info_total_course_points= ""  
        info_assigned_points= ""  

        # Dynamically fetch the points for each point name
        for i, point_name in enumerate(typepoint_names):
            point_field = f'Points{chr(65 + i)}'  # PointsA, PointsB, etc.
            point_value = getattr(course_year, point_field, None)
            points[point_name] = point_value if point_value is not None else 0  # Use 0 if None
            total_course_points += points[point_name]  # Sum the points
            
            # Add the point name and value to the string in the format "Teoria: 5"
            info_assigned_points += f"{point_name}: {points[point_name]}, "

        # Remove trailing comma and space from points_string
        info_assigned_points = info_assigned_points.strip(', ')

        assignments = Assigment.objects.filter(CourseYear=course_year)  # Get all assignments for the course_year
        for assignment in assignments:
            for i, point_name in enumerate(typepoint_names):
                point_field = f'Points{chr(65 + i)}'  # PointsA, PointsB, etc.
                assigned_point_value = getattr(assignment, point_field, None)
                if assigned_point_value is not None:
                    total_assigned_points += assigned_point_value 

        # Append course info along with points and total points
        course_data.append({
            'degree': course_year.Course.Degree.NameDegree,
            'course': course_year.Course.NameCourse,
            'semester': course_year.Semester,
            'year':course_year.Year,
            'points': points,
            'total_course_points': total_course_points,
            'total_assigned_points': total_assigned_points,
            'info_points_assigned': info_assigned_points, 
            'info_total_course_points': info_total_course_points, 
        })

    # Prepare context to pass courses to the template
    context = {
        'course_data': course_data,  # List of courses with their info
        'section': section,
        'year': year,
    }   
    return render(request, 'section_courses_assign/courses_assign_list_actions.html', context)
