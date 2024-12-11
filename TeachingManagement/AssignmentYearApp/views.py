
from django.shortcuts import render,redirect,get_object_or_404
from .utils import get_sectionchief_section
from AcademicInfoApp.models import Course,Degree,Year,School
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
    section = get_sectionchief_section(user)  # Call the utility function to fetch the section

    context = {'section': section }
    return render(request, 'test_sectionchief_info.html', context)

# COURSES found in that SECTION - IN ALL SCHOOLS - IN ALL DEGREES
def section_courses_list(request):
    user=request.user

    section= get_sectionchief_section(user) # return the section of the chief

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
        'PointsA': typepoints_section.NamePointsA if typepoints_section else None,
        'PointsB': typepoints_section.NamePointsB if typepoints_section else None,
        'PointsC': typepoints_section.NamePointsC if typepoints_section else None,
        'PointsD': typepoints_section.NamePointsD if typepoints_section else None,
        'PointsE': typepoints_section.NamePointsE if typepoints_section else None,
        'PointsF': typepoints_section.NamePointsF if typepoints_section else None,
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
        'PointsA': typepoints_section.NamePointsA if typepoints_section else None,
        'PointsB': typepoints_section.NamePointsB if typepoints_section else None,
        'PointsC': typepoints_section.NamePointsC if typepoints_section else None,
        'PointsD': typepoints_section.NamePointsD if typepoints_section else None,
        'PointsE': typepoints_section.NamePointsE if typepoints_section else None,
        'PointsF': typepoints_section.NamePointsF if typepoints_section else None,
    }
    #Only save the names of the groups that are not None
    for field, point_name in typepoints_fields.items():
        if point_name is not None:
            typepoint_names_assigned[field] = point_name
    
    #return TOTALPOINTS from CourseYear
    total_points_sum=0
    total_points = {}
    for field, point_name in typepoint_names_assigned.items():
        point_value = getattr(course_year,field, 0) or 0
        total_points[point_name] = point_value
    
        total_points_sum = sum(value if value is not None else 0 for value in total_points.values())

    #return ASSIGNEDPOINTSS from assignment
    assigned_points_sum=0
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
        data['is_coordinator']=assignment.isCoordinator

        data['professor_name'] = assignment.Professor.name +" "+assignment.Professor.family_name
        data['professor_id'] = assignment.Professor.idProfessor
        
        for field, point_name in typepoint_names_assigned.items():
            value = getattr(assignment, field, None) or 0
            data[point_name] = value

        assignment_data.append(data)

    # Query for all professors that are either assigned or not assigned to the courseYear
    assigned_professors = Professor.objects.filter(
        idProfessor__in=Assignment.objects.filter(CourseYear=course_year).values('Professor_id')
    )

    unassigned_professors = Professor.objects.filter(isActive='yes').exclude(
        idProfessor__in=Assignment.objects.filter(CourseYear=course_year).values('Professor_id')
    )

    # Combine both assigned and unassigned professors into a single queryset
    all_professors = assigned_professors.union(unassigned_professors).order_by('family_name')

    professor_data = []
    for professor in all_professors:
        #get if its assigned already or not
        is_assigned = assigned_professors.filter(idProfessor=professor.idProfessor).exists()  # True if assigned, False otherwise

        # Get total points assigned to this professor in this section
        prof_total_points=0
        prof_assigned_points = 0

        prof_remaining_points=0

        #Get total points that are entered in CAPACITY - FREE points for that professor x year
        capacity_entry = Capacity.objects.filter(Professor=professor, Year=course_year.Year).first()
        if capacity_entry:
            prof_total_points = capacity_entry.Points or 0
        else:
            prof_total_points = 0

        #Get the total points assignated for that professor in that section that year
        section_capacity_entry = CapacitySection.objects.filter(Professor=professor, Section=section, Year=course_year.Year).first()
        if section_capacity_entry:
            prof_assigned_points = section_capacity_entry.Points or 0
        else:
            prof_assigned_points = 0

        #Get all the points already assigned for that professor that year in that section
        assigned_points_in_courseyear = Assignment.objects.filter(
            Professor=professor,  CourseYear__Course__Degree__School__Section=section, CourseYear__Year=course_year.Year,  
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
            'is_assigned': is_assigned, 

            'prof_remaining_points': prof_remaining_points,
            'prof_total_points':prof_total_points,
            'prof_assigned_points': prof_assigned_points,

            'languages_list': languages_list,
            'fields_list': fields_list,
        })
    
    professor_data = sorted(professor_data, key=lambda x: x['is_assigned'], reverse=True)


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
        isCoordinator=False,  # Set IsCoordinator to False as per requirement
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
                        setattr(assignment, point_field, float(form_value) if form_value else None)
                    else:
                        setattr(assignment, point_field, None)  
           
            # Update Is Coordinator field
            is_coordinator = request.POST.get('is_coordinator')
            if is_coordinator == 'yes':
                assignment.isCoordinator = True
            elif is_coordinator == 'no':
                assignment.isCoordinator = False

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

        assignment.delete()
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
            messages.success(request, f"El comentari s'ha actualitzat correctament.")
        else:  # If  comment empty
            course_year.Comment = None
            messages.warning(request, "El comentari s'ha eliminat correctament.")
            
        course_year.save()
    return redirect('courseyear_show', idCourseYear=idCourseYear)


def section_professors_list(request):
    user=request.user
    section= get_sectionchief_section(user) # return the section of the chief

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

        # Return NAMES of the TYPE of POINTS for the course's section and year
    typepoints_section = TypePoints.objects.filter(
        Section=section,
        Year=year_obj
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

    #get all the scools in that section
    all_schools=School.objects.filter(Section=section)
   
    all_professors = Professor.objects.filter(isActive='yes').order_by('family_name')
    
    professor_data = []
    for professor in all_professors:
        # Get total points assigned to this professor in this section       
        prof_total_points=0
        prof_remaining_points=0

        # Get total points assigned to this professor in this section for Q1 and Q2
        assigned_points_in_courseyear = Assignment.objects.filter(
            Professor=professor,
            CourseYear__Course__Degree__School__Section=section,
            CourseYear__Year=year_obj
        )

        q1_points = assigned_points_in_courseyear.filter(CourseYear__Semester='Q1').aggregate(
            total=(
                Sum('PointsA', default=0) +
                Sum('PointsB', default=0) +
                Sum('PointsC', default=0) +
                Sum('PointsD', default=0) +
                Sum('PointsE', default=0) +
                Sum('PointsF', default=0)
            )
        )['total'] or 0        

        q2_points = assigned_points_in_courseyear.filter(CourseYear__Semester='Q2').aggregate(
            total=(
                Sum('PointsA', default=0) +
                Sum('PointsB', default=0) +
                Sum('PointsC', default=0) +
                Sum('PointsD', default=0) +
                Sum('PointsE', default=0) +
                Sum('PointsF', default=0)
            )
        )['total'] or 0

        #Get the total points assignated for that professor in  that year
        prof_capacity_entry = Capacity.objects.filter(Professor=professor, Year=year_obj).first()
        if prof_capacity_entry:
            prof_total_points = prof_capacity_entry.Points or 0
        else:
            prof_total_points = 0

        #Get the total points assignated for that professor in that section that year
        prof_capacitysection_entry = CapacitySection.objects.filter(Professor=professor,Section=section, Year=year_obj).first()
        if prof_capacitysection_entry:
            prof_capacitysection_points = prof_capacitysection_entry.Points or 0
        else:
            prof_capacitysection_points = 0

        # Calculate the points assigned (Q1 + Q2)
        total_assigned_points = q1_points + q2_points

        # Calculate remaining points (capacity - assigned)
        prof_remaining_points = prof_total_points - total_assigned_points

        # Calculate the percentage of points assigned versus total capacity
        if prof_total_points > 0:
            point_percentage = (total_assigned_points / prof_total_points) * 100
        else:
            point_percentage = 0

        #Get all the points assigned for that Professor for every the CourseYear for each School in this section
        points_for_schools=[]
        for school in all_schools:
            school_points = assigned_points_in_courseyear.filter(
                CourseYear__Course__Degree__School=school,
                Professor=professor
            ).aggregate(
                total=(
                    Sum('PointsA', default=0) +
                    Sum('PointsB', default=0) +
                    Sum('PointsC', default=0) +
                    Sum('PointsD', default=0) +
                    Sum('PointsE', default=0) +
                    Sum('PointsF', default=0)
                )
            )['total'] or 0

            points_for_schools.append({
                'school_name': school.NameSchool,  
                'points': round(school_points, 2)
            })
        

        professor_data.append({
            'professor_id': professor.idProfessor,
            'name': professor.name,

            'family_name': professor.family_name,
            'point_percentage':point_percentage,
            'pointsQ1': q1_points,
            'pointsQ2':q2_points,

            'total_capacity':prof_total_points,
            'capacity_section':prof_capacitysection_points,
            'points_not_assigned': prof_remaining_points,

            'points_for_schools': points_for_schools,
        })
    
    context = {
        'section':section,
        #list of all the schools in the section
        'schools_section':all_schools,
        #Table of professors candidates  to be assigned
        'professor_section_data': professor_data,
    }

    # Pass the course_year data to the template
    return render(request, 'professor_info_assign/professor_assign_info_list_actions.html', context)

#selecting the years
def select_years_for_duplication(request):

    if request.method == 'POST':
        source_year = request.POST.get('source_year')
        target_year = request.POST.get('target_year')

        if source_year and target_year:
            # Save selected years in the session
            request.session['source_year'] = source_year
            request.session['target_year'] = target_year

            # Redirect to any page after selecting years
            return redirect('section_courses_list')


    years = Year.objects.all().order_by('-Year').distinct()

    context = {
        'years': years,
    }

    return render(request, 'section_courses_assign/select_duplicate_years.html', context)

#duplicating the years
def duplicate_course_assignment(request, idCourseYear):
    # Get the course and years
    course_year = get_object_or_404(CourseYear, idCourseYear=idCourseYear)

    course=course_year.Course
    source_year = request.session.get('source_year') 
    target_year = request.session.get('target_year') 
    
    if not source_year or not target_year:
        messages.warning(request, "Els anys seleccionats no són vàlids. Selecciona els anys correctes.")
        return redirect('section_courses_list')

    source_year_obj = get_object_or_404(Year, Year=source_year)
    target_year_obj = get_object_or_404(Year, Year=target_year)

    # Get the CourseYear for the source year, course and semester
    course_years = CourseYear.objects.filter(Course=course, Year=source_year_obj, Semester=course_year.Semester)

    if not course_years.exists():
        messages.warinig(request, "No s'han trobat assignatures per duplicar en el curs i any seleccionats.")
        return redirect('section_courses_list')
    
    #Duplicate the typepoints for that section x year if does not exist
    section = course_year.Course.Degree.School.Section
    typepoints_section = get_object_or_404(TypePoints, Section=section, Year=source_year_obj)

    # Query the TypePoints for the source year and section
    existing_typepoints = TypePoints.objects.filter(Section=section, Year=source_year_obj)

    # Loop through each of the existing TypePoints and create a new one for the target year
    for typepoint in existing_typepoints:
        # Create a new TypePoints entry for the target year
        existing_typepoint = TypePoints.objects.filter(Section=typepoint.Section, Year=target_year_obj).first()
        
         # Create a new TypePoints entry
        if not existing_typepoint:
            TypePoints.objects.create(
                Section=typepoint.Section,  # The same section
                Year=target_year_obj,  # The target year
                NamePointsA=typepoints_section.NamePointsA,
                NamePointsB=typepoints_section.NamePointsB,
                NamePointsC=typepoints_section.NamePointsC,
                NamePointsD=typepoints_section.NamePointsD,
                NamePointsE=typepoints_section.NamePointsE,
                NamePointsF=typepoints_section.NamePointsF,
            )

    # Duplicate the course assignment
    for course_year in course_years:
        existing_course_year = CourseYear.objects.filter(
            Course=course_year.Course,
            Year=target_year_obj,
            Semester=course_year.Semester
        ).first()

        if not existing_course_year:
            # Create a new CourseYear entry
            new_course_year = CourseYear(
                Course=course_year.Course,
                Year=target_year_obj,
                Semester=course_year.Semester,
                PointsA=course_year.PointsA,
                PointsB=course_year.PointsB,
                PointsC=course_year.PointsC,
                PointsD=course_year.PointsD,
                PointsE=course_year.PointsE,
                PointsF=course_year.PointsF,
                Language=course_year.Language,
                Comment=course_year.Comment,
            )
            new_course_year.save()
        else:
            new_course_year = existing_course_year  

    #Duplicate the assigned professors for that course year 
    assignments = Assignment.objects.filter(CourseYear=course_year)
    for assignment in assignments:
        # Create a new assignment for the target year and target CourseYear
        Assignment.objects.update_or_create(
            CourseYear=new_course_year,
            Professor=assignment.Professor,  
            isCoordinator=assignment.isCoordinator, 
            PointsA=assignment.PointsA,
            PointsB=assignment.PointsB,
            PointsC=assignment.PointsC,
            PointsD=assignment.PointsD,
            PointsE=assignment.PointsE,
            PointsF=assignment.PointsF,
        )


    messages.success(request, f'Assignatures duplicades amb èxit de {source_year} a {target_year}.')
    return redirect('section_courses_list')
