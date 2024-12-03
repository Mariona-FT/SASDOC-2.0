
from django.shortcuts import render,redirect,get_object_or_404
from .utils import get_sectionchief_section
from AcademicInfoApp.models import Course,Degree,Year
from ProfSectionCapacityApp.models import CourseYear,TypePoints
from UsersApp.models import Professor,ProfessorField,ProfessorLanguage
from ProfSectionCapacityApp.models import Capacity,Free,CapacitySection
from .models import Assignment
from django.urls import reverse
from django.http import JsonResponse
import json
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum

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
    
    typepoint_names_assigned={}
    #Dicc to have the names linked for the possible points
    typepoints_fields = {
        'PointsA': typepoints_section.NamePointsA,
        'PointsB': typepoints_section.NamePointsB,
        'PointsC': typepoints_section.NamePointsC,
        'PointsD': typepoints_section.NamePointsD,
        'PointsE': typepoints_section.NamePointsE,
        'PointsF': typepoints_section.NamePointsF
    }
    #Only save the names of the groups that are not None
    for field, point_name in typepoints_fields.items():
        if point_name is not None:
            typepoint_names_assigned[field] = point_name
    
    course_data = [] #all info of ONE COURSE
   
    for course_year in course_years:
        total_points = {}
        total_course_points = 0         #total points TO assign in the course - initial points
        total_assigned_points = 0       #total ALREADY assigned points - where professors wil be assigned
        
        # Return info of TOTAL POINTS - that will need to be assigned that Course year
        total_points = {}
        for field, point_name in typepoint_names_assigned.items():
            point_value = getattr(course_year,field, 0) or 0
            total_points[point_name] = point_value
        
            total_course_points = sum(value if value is not None else 0 for value in total_points.values())
        
        #Return info of INFO POINTS ALREADY ASSIGNED x professor that Course year
        #return ASSIGNEDPOINTSS from assignment
        assigned_points = {name: 0 for name in typepoint_names}
        assignments = Assignment.objects.filter(CourseYear=course_year)

        for assignment in assignments:
            for field, point_name in typepoint_names_assigned.items():
                assigned_value = getattr(assignment, field, 0) or 0
                if assigned_value is not None:
                    assigned_points[point_name] += assigned_value

        total_assigned_points = sum(value if value is not None else 0 for value in assigned_points.values())
        
        # Create formatted string for each point type in "Group: assigned/total" format
        points_summary = ""
        # for point_name in typepoint_names:
        for field, point_name in typepoint_names_assigned.items():
            assigned_value = assigned_points.get(point_name, 0)
            total_value = total_points.get(point_name, 0)
            points_summary += f"{point_name}: {total_value}/{assigned_value} , "

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

    section = course_year.Course.Degree.School.Section
    # Return NAMES of the TYPE of POINTS for the course's section and year
    typepoints_section = TypePoints.objects.filter(
        Section=section,
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

    typepoint_names_assigned={}
    #Dicc to have the names linked for the possible points
    typepoints_fields = {
        'PointsA': typepoints_section.NamePointsA,
        'PointsB': typepoints_section.NamePointsB,
        'PointsC': typepoints_section.NamePointsC,
        'PointsD': typepoints_section.NamePointsD,
        'PointsE': typepoints_section.NamePointsE,
        'PointsF': typepoints_section.NamePointsF
    }
    #Only save the names of the groups that are not None
    for field, point_name in typepoints_fields.items():
        if point_name is not None:
            typepoint_names_assigned[field] = point_name
    
    #return TOTALPOINTS from CourseYear
    total_points = {}
    for field, point_name in typepoint_names_assigned.items():
        point_value = getattr(course_year,field, 0) or 0
        total_points[point_name] = point_value
    
        total_points_sum = sum(value if value is not None else 0 for value in total_points.values())

    #return ASSIGNEDPOINTSS from assignment
    assigned_points = {name: 0 for name in typepoint_names}
    assignments = Assignment.objects.filter(CourseYear=course_year)

    for assignment in assignments:
        for field, point_name in typepoint_names_assigned.items():
            assigned_value = getattr(assignment, field, 0) or 0
            if assigned_value is not None:
                assigned_points[point_name] += assigned_value

    assigned_points_sum = sum(value if value is not None else 0 for value in assigned_points.values())


    #return ONLY the ASSIGNED PROFESSORS - it will be in the Assignment table in that CourseYear
    assignments = Assignment.objects.filter(CourseYear=course_year)

    #Save the info of the PROFESSORS already assgned
    assignment_data = []
    for assignment in assignments:
        data = {}
        data['id']=assignment.idAssignment
        data['is_coordinator']=assignment.IsCoordinator

        data['professor_name'] = assignment.Professor.name +" "+assignment.Professor.family_name
        data['professor_id'] = assignment.Professor.idProfessor
        
        for field, point_name in typepoint_names_assigned.items():
            value = getattr(assignment, field, None) or 0
            data[point_name] = value

        assignment_data.append(data)

    #return PROFESSORS that are NOT ASSIGNED in that courseYear
    professors = Professor.objects.filter(isActive='yes').exclude(
        idProfessor__in=Assignment.objects.filter(CourseYear=course_year).values('Professor_id')
    ).order_by('family_name')

    professor_data = []
    for professor in professors:
        # Get total points assigned to this professor in this section
        prof_total_points=0
        prof_assigned_points = 0

        prof_remaining_points=0

        #Get total points that are entered in CAPACITY - FREE points for that professor x year
        capacity_entry = Capacity.objects.filter(Professor=professor, Year=course_year.Year).first()
        if capacity_entry:
            total_capacity_points = capacity_entry.Points or 0
        else:
            total_capacity_points = 0

        free_entries = Free.objects.filter(Professor=professor, Year=course_year.Year)
        total_free_points = free_entries.aggregate(total_free_points=Sum('PointsFree'))['total_free_points'] or 0

        #total points is the capacity - points liberated for that year
        prof_total_points =  total_capacity_points - total_free_points

        #Get the total points assignated for that professor in that section that year
        section_capacity_entry = CapacitySection.objects.filter(Professor=professor, Section=section, Year=course_year.Year).first()
        if section_capacity_entry:
            prof_assigned_points = section_capacity_entry.Points or 0
        else:
            prof_assigned_points = 0

        #Get all the points already assigned for that professor that year in that section
        assigned_points_in_courseyear = Assignment.objects.filter(
            Professor=professor,  CourseYear__Course__Degree__School__Section=section, 
        )

        total_assigned_points =0
       # Aggregate the sum of each point field
        for field, point_field_name in typepoint_names_assigned.items():
            total_points_for_field = assigned_points_in_courseyear.aggregate(
                total_points=Sum(field)
            )['total_points'] or 0  # Sum points for this specific field
            total_assigned_points += total_points_for_field

        prof_remaining_points=total_assigned_points - prof_assigned_points

        # Get professor's languages and fields
        languages = ProfessorLanguage.objects.filter(Professor=professor)
        fields = ProfessorField.objects.filter(Professor=professor)

        # If no languages or fields are found, set them to an empty string
        languages_list = ', '.join([language.Language.Language for language in languages]) if languages else "-"
        fields_list = ', '.join([field.Field.NameField for field in fields]) if fields else "-"


        professor_data.append({
            'professor_id': professor.idProfessor,
            'name': professor.name,
            'family_name': professor.family_name,
            
            'prof_remaining_points': prof_remaining_points,
            'prof_total_points':prof_total_points,
            'prof_assigned_points': prof_assigned_points,

            'languages_list': languages_list,
            'fields_list': fields_list,
        })


    context = {
        'course_year': course_year,
        #list of the type of points-the name given
        'typepoint_names_assigned': typepoint_names_assigned,

        #Table of actual total points and assigned points
        'total_points': total_points,
        'assigned_points': assigned_points,
        'total_points_sum':total_points_sum,
        'assigned_points_sum': assigned_points_sum,
        
        #Table professors assigned
        'assignment_data': assignment_data,

        #Table of professors candidates  to be assigned
        'professor_data': professor_data,
    }

    # Pass the course_year data to the template
    return render(request, 'section_courses_assign/overview_course_assign.html', context)

def assign_professor(request, professor_id, course_year_id):
    course_year = get_object_or_404(CourseYear, pk=course_year_id)
    professor = get_object_or_404(Professor, pk=professor_id)

    # Create a new assignment for the professor in the given course year
    assignment = Assignment(
        Professor=professor,
        CourseYear=course_year,
        IsCoordinator=False,  # Set IsCoordinator to False as per requirement
        # Set all points to null (or default to 0)
        PointsA=None,
        PointsB=None,
        PointsC=None,
        PointsD=None,
        PointsE=None,
        PointsF=None,
    )
    assignment.save()

    # Redirect back to the assign_candidates page
    return redirect('courseyear_show', idCourseYear=course_year_id)

@csrf_exempt
def update_assignment(request,idAssignment):
    assignment = get_object_or_404(Assignment, pk=idAssignment)
    
    if request.method == 'POST':
        try:
            course_year = assignment.CourseYear
            section = course_year.Course.Degree.School.Section

            # have  the associated TypePoints for the section and year
            typepoints_section = TypePoints.objects.filter(
                Section=section,
                Year=course_year.Year
            ).first()

            #extract the names of typepoints for that section
            typepoint_names_assigned = {}
            if typepoints_section:
                typepoint_fields = {
                    'PointsA': typepoints_section.NamePointsA,
                    'PointsB': typepoints_section.NamePointsB,
                    'PointsC': typepoints_section.NamePointsC,
                    'PointsD': typepoints_section.NamePointsD,
                    'PointsE': typepoints_section.NamePointsE,
                    'PointsF': typepoints_section.NamePointsF,
                }

            # for the diferent points PointA-F used as the typepoints of that section NamePointsA-F 
            # SAVE the info of the FORM in the table ASSIGNMENT for PointsA-F  
            for point_field, point_name in typepoint_fields.items():
                if point_name:  # If a point name is defined
                    form_value = request.POST.get(point_name)
                    if form_value is not None:
                        setattr(assignment, point_field, int(form_value) if form_value else None)
                    else:
                        setattr(assignment, point_field, None)  
           
            # Update Is Coordinator field
            is_coordinator = request.POST.get('is_coordinator')
            if is_coordinator == 'yes':
                assignment.IsCoordinator = True
            elif is_coordinator == 'no':
                assignment.IsCoordinator = False

            # Save the updated assignment object
            assignment.save()
        
            messages.success(request, 'Assignació modificada correctament.')
            return redirect('courseyear_show', idCourseYear=course_year.idCourseYear)

        except Exception as e:
            messages.error(request, f"Error al modificar l'Assignació: {str(e)}")
            return redirect('courseyear_show', idCourseYear=course_year.idCourseYear)
    else:
        messages.error(request, 'Mètode del Form invàlid.')
        return redirect('courseyear_show', idCourseYear=assignment.CourseYear.idCourseYear)


@csrf_exempt
def delete_courseyear_professor(request, idProfessor, idCourseYear):
    # Retrieve the professor and course year
    professor = get_object_or_404(Professor, idProfessor=idProfessor)
    course_year = get_object_or_404(CourseYear, pk=idCourseYear)

    try:
        assignment = Assignment.objects.get(Professor=professor, CourseYear=course_year)
        print("assigned to delete",assignment)

        #assignment.delete()
        messages.success(request, 'Assignació del Professor correctament eliminada.')
    except Exception as e:
        messages.error(request, f"Error: No s'ha pogut eliminar l'assignació triada ({e}).")

    return redirect('courseyear_show', idCourseYear=idCourseYear)

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

