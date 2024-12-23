from django.shortcuts import render, redirect,get_object_or_404
from .forms import CapacityForm, FreeForm, CapacitySectionForm,TypePointsForm,CourseYearForm
from .models import Professor, Capacity, Free, CapacitySection,TypePoints,CourseYear
from UsersApp.models import Professor
from AcademicInfoApp.models import Section,Year
from django.contrib import messages
from itertools import chain
from django.db.models import Sum


# Create your views here.

#PROFESSORS
def capacityprofessor_list(request):
    # Get all years for capacity selection
    available_years = Year.objects.all().order_by('-Year').distinct()
    selected_year_id = request.GET.get('year') #year id
    selected_year = None # object year

    # Get all professors ordered by family name
    all_sections = Section.objects.all()
    professor_data = []

    #Get year selected - if not selected most recent year
    if selected_year_id:
        try:
            selected_year = Year.objects.get(pk=int(selected_year_id))
        except Year.DoesNotExist:
            messages.error(request, "Curs acadèmic seleccionat no existeix.")
    
    if not selected_year:
        selected_year = Year.objects.order_by('-Year').first()
    
    # Determine if the selected year is the most recent year
    is_most_recent_year = selected_year == Year.objects.order_by('-Year').first()
        
    # Get capacities for the selected year
    capacities = Capacity.objects.filter(Year_id=selected_year.idYear).order_by('Professor__family_name')
    
    # Process each capacity
    for capacity in capacities:
        professor = capacity.Professor
        free_points = Free.objects.filter(Professor=professor, Year=selected_year).aggregate(free_points=Sum('PointsFree'))['free_points'] or 0
        
        # Initialize section points list
        section_points = [(section.LetterSection, 0) for section in all_sections]
        
        # Update section points based on CapacitySection entries
        for section_entry in CapacitySection.objects.filter(Professor=professor, Year=selected_year):
            section_letter = section_entry.Section.LetterSection
            section_points = [(letter, section_entry.Points if letter == section_letter else points) for letter, points in section_points]
        
        # Calculate the section points sum
        section_points_sum = sum(points for _, points in section_points)

        #return the number of balanced points
        balance= capacity.Points - free_points - section_points_sum

        # Append data for the professor with capacity
        professor_data.append({
            'professor': professor,
            'year': selected_year.Year,
            'capacity_points': capacity.Points,
            'free_points': free_points,
            'section_points': section_points,
            'balance':balance,
        })
    
    # If the selected year is the most recent year, include professors without capacities for this year
    if is_most_recent_year:
        professors_without_capacity = Professor.objects.exclude(idProfessor__in=capacities.values('Professor')).order_by('family_name')
        
        for professor in professors_without_capacity:
            # Initialize section points with zeroes for professors without capacities
            free_points = Free.objects.filter(Professor=professor, Year=selected_year).aggregate(free_points=Sum('PointsFree'))['free_points'] or 0

            section_points = [(section.LetterSection, 0) for section in all_sections]
           
            for section_entry in CapacitySection.objects.filter(Professor=professor, Year=selected_year):
                section_letter = section_entry.Section.LetterSection
                section_points = [(letter, section_entry.Points if letter == section_letter else points) for letter, points in section_points]
        
            # Calculate the section points sum
            section_points_sum = sum(points for _, points in section_points)
            
            # Set balance to "NA" for professors without capacity
            balance = "NA"  

            
            # Append data for professors without capacity
            professor_data.append({
                'professor': professor,
                'year': "NA",
                'capacity_points': 0,
                'free_points': free_points,
                'section_points': section_points,
                'balance':balance,
            })

    return render(request, 'professor_capacity/capacityprofessor_list_actions.html', {
        'professor_data': professor_data,
        'all_sections': all_sections,
        'available_years': available_years,
        'selected_year': selected_year,
    })

def capacityprofessor_select(request):
    professors = Professor.objects.all().order_by('family_name')  # Fetch all professors
    return render(request, 'professor_capacity/new_professor_capacity.html', {'professors': professors})

#INFO ONLY ONE PROFESSOR 
def capacityprofessor_show(request,idProfessor=None):
# Retrieve the professor instance if idProfessor is provided
    professor = get_object_or_404(Professor, pk=idProfessor) if idProfessor else None

    # Initialize forms for each model
    capacity_form = CapacityForm(request.POST or None, prefix='capacity')
    free_form = FreeForm(request.POST or None, prefix='free')
    capacity_section_form = CapacitySectionForm(request.POST or None, prefix='capacity_section')

  
    # Get the selected year from the GET parameters
    selected_year_id = request.GET.get('year')  # Year id from the URL or form
    selected_year = None  # Object year

    # Get the most recent year if no year is selected
    if selected_year_id:
        try:
            selected_year = Year.objects.get(pk=int(selected_year_id))
        except Year.DoesNotExist:
           messages.error(request, "Curs acadèmic seleccionat no existeix.")
    
    if not selected_year:
        most_recent_capacity = Capacity.objects.filter(Professor_id=idProfessor).order_by('Year').first()
        if most_recent_capacity:
            selected_year = most_recent_capacity.Year  # Assign the year from the most recent capacity entry
        else:
            selected_year = None 

    # Filter capacity, free, and capacity_section entries by the selected year
    capacities = Capacity.objects.filter(Professor=professor, Year=selected_year).order_by('-Year__Year')
    frees = Free.objects.filter(Professor=professor, Year=selected_year).order_by('-Year__Year')
    capacity_sections = CapacitySection.objects.filter(Professor=professor, Year=selected_year).order_by('-Year__Year')
  

    # Calculate the balance
    capacity_points = sum(c.Points for c in capacities)
    free_points = sum(f.PointsFree for f in frees)
    section_points_sum = sum(s.Points for s in capacity_sections)

    balance = capacity_points - free_points - section_points_sum

    # Extract unique Year objects from the available capacities, frees, and capacity_sections
    # We will query the Year model directly and then deduplicate and sort the results
    years_from_capacities = Capacity.objects.filter(Professor=professor).values_list('Year', flat=True)
    years_from_frees = Free.objects.filter(Professor=professor).values_list('Year', flat=True)
    years_from_capacity_sections = CapacitySection.objects.filter(Professor=professor).values_list('Year', flat=True)

    # Combine all the year IDs and retrieve the corresponding Year objects
    unique_year_ids = set(chain(years_from_capacities, years_from_frees, years_from_capacity_sections))

    # Query Year objects corresponding to these IDs
    available_years = Year.objects.filter(idYear__in=unique_year_ids).order_by('-Year')
    
    context = {
        'capacity_form': capacity_form,
        'free_form': free_form,
        'capacity_section_form': capacity_section_form,
        'professor': professor,
        'capacities': capacities,
        'frees': frees,
        'capacity_sections': capacity_sections,
        'balance':balance,
        'available_years': available_years,
        'selected_year': selected_year, 
    }

    return render(request, 'professor_capacity/overview_professor_capacity.html', context)

#CAPACITY
# Create a new Capacity entry
def create_capacity(request, idProfessor):
    professor = get_object_or_404(Professor, pk=idProfessor)

    if request.method == 'POST':
        form = CapacityForm(request.POST,professor=professor)
        if form.is_valid():
            form.save()  
            messages.success(request, 'Punts totals correctament creats.')
            return redirect('capacityprofessor_show', idProfessor=idProfessor)
    else:
        form = CapacityForm(professor=professor)

    return render(request, 'professor_capacity/professor_capacity_form.html', {'form': form, 'professor': professor})

# Edit an existing Capacity entry
def edit_capacity(request, idCapacity):
    capacity = get_object_or_404(Capacity, pk=idCapacity)
    idProfessor = capacity.Professor.idProfessor  

    if request.method == 'POST':
        form = CapacityForm(request.POST, instance=capacity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Punts totals correctament editats.')
            return redirect('capacityprofessor_show', idProfessor=idProfessor)
    else:
        form = CapacityForm(instance=capacity)

    return render(request, 'professor_capacity/professor_capacity_form.html', {'form': form, 'professor': capacity.Professor, 'year': capacity.Year})

def delete_capacity(request, idCapacity):
    capacity = get_object_or_404(Capacity, pk=idCapacity)
    idProfessor = capacity.Professor.idProfessor  
    try:
        capacity.delete()
        messages.success(request, 'Punts totals correctament eliminats.')
    except Exception as e:
        messages.error(request, f"Error: No s'ha pogut eliminar els punts totals ({e}).")

    return redirect('capacityprofessor_show', idProfessor=idProfessor)

#FREE
# Create a new Free entry
def create_free(request, idProfessor):
    professor = get_object_or_404(Professor, pk=idProfessor)

    if request.method == 'POST':
        form = FreeForm(request.POST,professor=professor)
        if form.is_valid():
            form.save()
            messages.success(request, "Punts d'alliberació correctament creats.")
            return redirect('capacityprofessor_show', idProfessor=idProfessor)
    else:
        form = FreeForm(professor=professor)

    return render(request, 'professor_capacity/professor_free_capacity_form.html', {'form': form, 'professor': professor})

# Edit an existing Capacity entry
def edit_free(request, idFree):
    free = get_object_or_404(Free, pk=idFree)
    idProfessor = free.Professor.idProfessor  

    if request.method == 'POST':
        form = FreeForm(request.POST, instance=free)
        if form.is_valid():
            form.save()
            messages.success(request, "Punts d'alliberació correctament editats.")
            return redirect('capacityprofessor_show', idProfessor=idProfessor)
    else:
        form = FreeForm(instance=free)

    return render(request, 'professor_capacity/professor_free_capacity_form.html', {'form': form, 'professor': free.Professor, 'year': free.Year})

def delete_free(request, idFree):
    free = get_object_or_404(Free, pk=idFree)
    idProfessor = free.Professor.idProfessor  
    try:
        free.delete()
        messages.success(request, "Punts d'alliberació correctament eliminats.")
    except Exception as e:
        messages.error(request, f"Error: No s'ha pogut eliminar els punts d'alliberaciós ({e}).")

    return redirect('capacityprofessor_show', idProfessor=idProfessor)

#CAPACITY SECTION
# Create a new Capacity section entry
def create_capacity_section(request, idProfessor):
    professor = get_object_or_404(Professor, pk=idProfessor)

    if request.method == 'POST':
        form = CapacitySectionForm(request.POST,professor=professor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Punts per seccions correctament creats.')
            return redirect('capacityprofessor_show', idProfessor=idProfessor)
    else:
        form = CapacitySectionForm(professor=professor)

    return render(request, 'professor_capacity/professor_capacity_section_form.html', {'form': form, 'professor': professor})

# Edit an existing Capacity section entry
def edit_capacity_section(request, idCapacitySection):
    capsection = get_object_or_404(CapacitySection, pk=idCapacitySection)
    idProfessor = capsection.Professor.idProfessor  

    if request.method == 'POST':
        form = CapacitySectionForm(request.POST, instance=capsection,professor=capsection.Professor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Punts per seccions correctament editats.')
            return redirect('capacityprofessor_show', idProfessor=idProfessor)
    else:
        form = CapacitySectionForm(instance=capsection,professor=capsection.Professor)

    return render(request, 'professor_capacity/professor_capacity_form.html', {'form': form, 'professor': capsection.Professor, 'year': capsection.Year})

def delete_capacity_section(request, idCapacitySection):
    capsection = get_object_or_404(CapacitySection, pk=idCapacitySection)
    idProfessor = capsection.Professor.idProfessor  
    try:
        capsection.delete()
        messages.success(request, 'Punts per seccions correctament eliminat.')
    except Exception as e:
        messages.error(request, f"Error: No s'ha pogut eliminar els punts per seccions ({e}).")

    return redirect('capacityprofessor_show', idProfessor=idProfessor)

#SECTIONS
#Get all the capacity for each section for selected year
def section_typepoints_list(request):
    # Get all years for capacity selection
    available_years = Year.objects.all().order_by('-Year').distinct()
   
    selected_year_id = None #year id
    selected_year = None # object year

 # Get selected year or default to the most recent year
    selected_year_id = request.GET.get('year')
    try:
        selected_year_id = int(selected_year_id) if selected_year_id else 0
        selected_year = Year.objects.get(pk=selected_year_id)
    except (ValueError, Year.DoesNotExist):
        selected_year = Year.objects.order_by('-Year').first()
        if not selected_year:
            messages.error(request, "No hi ha cursos acadèmics disponibles.")
            return render(request, 'section_typepoints/section_typepoints_list_actions.html', {'available_years': available_years})
    
    # Determine if the selected year is the most recent year
    is_most_recent_year = selected_year == Year.objects.order_by('-Year').first()
    
    all_typepoints = TypePoints.objects.filter(Year_id=selected_year.idYear)

    if not all_typepoints.exists():
        messages.warning(request, "No s'han trobat nomenclatures per les seccions en el curs acadèmic seleccionat.")


    section_typepoints_info = []
    for typepoint in all_typepoints:
        section = typepoint.Section
        section_info = {
            'NameSection': getattr(section, 'NameSection', 'N/A'),  # Section Name
            'LetterSection': getattr(section, 'LetterSection', 'N/A'),  # Section Letter
            'Typepoint_id': typepoint.idTypePoints,
            'Year': typepoint.Year,
            'NamePointsA': typepoint.NamePointsA or '-',  # Points A
            'NamePointsB': typepoint.NamePointsB or '-',  # Points B
            'NamePointsC': typepoint.NamePointsC or '-',  # Points C
            'NamePointsD': typepoint.NamePointsD or '-',  # Points D
            'NamePointsE': typepoint.NamePointsE or '-',  # Points E
            'NamePointsF': typepoint.NamePointsF or '-',  # Points F
        }
        section_typepoints_info.append(section_info)

    context = {
        'available_years': available_years,
        'selected_year': selected_year,
        'is_most_recent_year': is_most_recent_year,
        'section_typepoints_info': section_typepoints_info,
    }
    
    return render(request, 'section_typepoints/section_typepoints_list_actions.html', context)

# Create a new TypePoints entry
def create_typepoints(request):
    if request.method == 'POST':
        form = TypePointsForm(request.POST)
        if form.is_valid():
            form.save()  
            messages.success(request, 'Nomenclatura de la secció correctament creada.')
            return redirect('sectiontypepoints_list')
        else:
            messages.error(request, "Hi ha errors al formulari. Revisa els camps.")

    else:
        form = TypePointsForm()

    return render(request, 'section_typepoints/section_typepoints_form.html', {'form': form})


def edit_typepoints(request, idTypePoints):
    typepoints = get_object_or_404(TypePoints, idTypePoints=idTypePoints)

    if request.method == 'POST':
        form = TypePointsForm(request.POST, instance=typepoints)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nomenclatura de la secció correctament editada.')
            return redirect('sectiontypepoints_list')
        else:
            messages.error(request, "Hi ha errors al formulari. Revisa els camps.")

    else:
        form = TypePointsForm(instance=typepoints)

    return render(request, 'section_typepoints/section_typepoints_form.html', {'form': form, 'section': typepoints.Section, 'year': typepoints.Year})

# Delete an existing TypePoints entry
def delete_typepoints(request, idTypePoints):
    typepoints = get_object_or_404(TypePoints, pk=idTypePoints)

    try:
        typepoints.delete()
        messages.success(request, 'Nomenclatura de la secció correctament eliminada.')
    except Exception as e:
        messages.error(request, f"Error: No s'ha pogut eliminar la nomenclatura ({e}).")

    return redirect('sectiontypepoints_list')


## FUNCTIONS FOR COURSES X YEAR
def course_year_list(request):
    # Get all years for capacity selection
    available_years = Year.objects.all().order_by('-Year').distinct()
   
    selected_year_id = None #year id
    selected_year = None # object year

 # Get selected year or default to the most recent year
    selected_year_id = request.GET.get('year')
    try:
        selected_year_id = int(selected_year_id) if selected_year_id else 0
        selected_year = Year.objects.get(pk=selected_year_id)
    except (ValueError, Year.DoesNotExist):
        selected_year = Year.objects.order_by('-Year').first()
        if not selected_year:
            messages.error(request, "No hi ha anys disponibles.")
            return render(request, 'course_capacity/capacity_course_list_actions.html', {'available_years': available_years})
    
    # Determine if the selected year is the most recent year
    is_most_recent_year = selected_year == Year.objects.order_by('-Year').first()

    all_courseyears=CourseYear.objects.filter(Year_id=selected_year.idYear).order_by('Course')

    for course_year in all_courseyears:
        course_year.TotalPoints = sum([
                course_year.PointsA or 0,
                course_year.PointsB or 0,
                course_year.PointsC or 0,
                course_year.PointsD or 0,
                course_year.PointsE or 0,
                course_year.PointsF or 0
            ])
        
    # Check for empty course list
    if not all_courseyears.exists():
        messages.warning(request, "No hi ha cursos amb puntuació disponibles per l'any seleccionat.")
   
    context = {
        'available_years': available_years,
        'selected_year': selected_year,
        'is_most_recent_year': is_most_recent_year,
        'course_years': all_courseyears,
    }

    return render(request, 'course_capacity/capacity_course_list_actions.html', context)

#Create a new Course Year
def create_courseyear(request):
    if request.method == 'POST':
        form = CourseYearForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Puntuació del Curs creada correctament.')
            return redirect('courseyear_list')
        else:
            messages.error(request, "Hi ha errors al formulari. Revisa els camps.")

    else:
        form = CourseYearForm()

    return render(request, 'course_capacity/capacity_course_form.html', {'form': form})

def edit_courseyear(request, idCourseYear):
    course_year = get_object_or_404(CourseYear, idCourseYear=idCourseYear)

    if request.method == 'POST':
        form = CourseYearForm(request.POST, instance=course_year)
        if form.is_valid():
            form.save()
            messages.success(request, 'Puntuació del Curs editat correctament.')
            return redirect('courseyear_list')
        else:
            messages.error(request, "Hi ha errors al formulari. Revisa els camps.")

    else:
        form = CourseYearForm(instance=course_year)

    return render(request, 'course_capacity/capacity_course_form.html', {'form': form, 'course_year': course_year})

#Delete an existing Course Year entry
def delete_courseyear(request, idCourseYear):
    course_year = get_object_or_404(CourseYear, idCourseYear=idCourseYear)

    try:
        course_year.delete()
        messages.success(request, 'Puntuació del Curs eliminada correctament.')
    except Exception as e:
        messages.error(request, f"Error: No s'ha pogut eliminar el curs. Motiu: {str(e)}")

    return redirect('courseyear_list')