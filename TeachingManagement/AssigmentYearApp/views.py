
from django.shortcuts import render,redirect
from .utils import get_sectionchief_section
from AcademicInfoApp.models import Course,Degree
from ProfSectionCapacityApp.models import CourseYear,TypePoints

# Create your views here.

def check_section_chief_section(request):
    user = request.user
    section,year = get_sectionchief_section(user)  # Call the utility function to fetch the section

    context = {'section': section,'year':year}


    return render(request, 'test_sectionchief_info.html', context)

# COURSES found in that SECTION - IN ALL SCHOOLS - IN ALL DEGREES
def section_courses_list(request):
    user=request.user
    section,year= get_sectionchief_section(user) # return the section of the chief

    # Fetch courses associated with the section, year, and relevant schools/degrees
    course_years  = CourseYear.objects.filter(
        Course__Degree__School__Section=section,  # Filter by Section
        Year=year  # Filter by Year
    ).select_related('Course', 'Year', 'Course__Degree')

   
    typepoints_section=TypePoints.objects.filter(
        Section=section,  # Filter by Section
        Year=year  # Filter by Year
    ).first()

    #extract the names of that section - only save the not empty names 
    typepoint_names = []
    if typepoints_section:
        typepoint_fields = ['NamePointsA', 'NamePointsB', 'NamePointsC', 'NamePointsD', 'NamePointsE', 'NamePointsF']
        for field in typepoint_fields:
            point_name = getattr(typepoints_section, field)
            if point_name:  # Check if the field is not empty or None
                typepoint_names.append(point_name)

    # Extract points for each course and add them to a list of dictionaries
    course_data = []
    for course_year in course_years:
        points = []
        # Dynamically fetch the points for each point name
        for i, point_name in enumerate(typepoint_names):
            point_field = f'Points{chr(65 + i)}'  # PointsA, PointsB, etc.
            points.append((point_name, getattr(course_year, point_field, None)))

        # Append course info along with the points
        course_data.append({
            'degree': course_year.Course.Degree.NameDegree,
            'course': course_year.Course.NameCourse,
            'semester': course_year.Semester,
            'points': points
        })

    # Prepare context to pass courses to the template
    context = {
        'course_data': course_data,  # List of courses with their points
        'typepoint_names': typepoint_names,  # List of point names
        'section': section,
        'year': year,
    }   
    return render(request, 'section_courses_assign/courses_assign_list_actions.html', context)
