from django.shortcuts import render, redirect,get_object_or_404
from .forms import CapacityForm, FreeForm, CapacitySectionForm
from .models import Professor, Capacity, Free, CapacitySection
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
    professors = Professor.objects.all().order_by('family_name')
    all_sections = Section.objects.all()
    professor_data = []

    #Get year selected - if not selected most recent year
    if selected_year_id:
        try:
            selected_year = Year.objects.get(pk=int(selected_year_id))
        except Year.DoesNotExist:
            messages.error(request, "Any seleccionat no existeix.")
    
    if not selected_year:
        selected_year = Year.objects.order_by('-Year').first()
    
    # Determine if the selected year is the most recent year
    is_most_recent_year = selected_year == Year.objects.order_by('-Year').first()
    
    all_sections = Section.objects.all()
    professor_data = [] #Dicc to save all info of the professors
    
    # Get capacities for the selected year
    capacities = Capacity.objects.filter(Year_id=selected_year.idYear).order_by('Professor__family_name')
    
    # Process each capacity
    for capacity in capacities:
        professor = capacity.Professor
        free_points = Free.objects.filter(Professor=professor, Year=selected_year).aggregate(free_points=Sum('PointsFree'))['free_points'] or 0
        
        # Initialize section points list
        section_points = [(section.NameSection, 0) for section in all_sections]
        
        # Update section points based on CapacitySection entries
        for section_entry in CapacitySection.objects.filter(Professor=professor, Year=selected_year):
            section_name = section_entry.Section.NameSection
            section_points = [(name, section_entry.Points if name == section_name else points) for name, points in section_points]
        
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
        professors_without_capacity = Professor.objects.exclude(idProfessor__in=capacities.values('Professor'))
        
        for professor in professors_without_capacity:
            # Initialize section points with zeroes for professors without capacities
            free_points = Free.objects.filter(Professor=professor, Year=selected_year).aggregate(free_points=Sum('PointsFree'))['free_points'] or 0

            section_points = [(section.NameSection, 0) for section in all_sections]
           
            for section_entry in CapacitySection.objects.filter(Professor=professor, Year=selected_year):
                section_name = section_entry.Section.NameSection
                section_points = [(name, section_entry.Points if name == section_name else points) for name, points in section_points]
        
             # Calculate the section points sum
            section_points_sum = sum(points for _, points in section_points)

            # Calculate the balance with zero capacity points (since no capacity entry exists)
            balance = 0 - free_points - section_points_sum
            
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
    professors = Professor.objects.all()  # Fetch all professors
    return render(request, 'professor_capacity/new_professor_capacity.html', {'professors': professors})

#INFO ONLY ONE PROFESSOR 
def capacityprofessor_create_edit(request,idProfessor=None):
    # Retrieve the professor instance if idProfessor is provided
    professor = get_object_or_404(Professor, pk=idProfessor) if idProfessor else None

    # Initialize forms for each model
    capacity_form = CapacityForm(request.POST or None, prefix='capacity')
    free_form = FreeForm(request.POST or None, prefix='free')
    capacity_section_form = CapacitySectionForm(request.POST or None, prefix='capacity_section')

    if request.method == 'POST':
        # Process each form
        if capacity_form.is_valid() and free_form.is_valid() and capacity_section_form.is_valid():
            # Save Capacity form
            capacity = capacity_form.save(commit=False)
            capacity.Professor = professor
            capacity.save()

            # Save Free form
            free = free_form.save(commit=False)
            free.Professor = professor
            free.save()

            # Save CapacitySection form
            capacity_section = capacity_section_form.save(commit=False)
            capacity_section.Professor = professor
            capacity_section.save()

            # Redirect to a success page or the same page with a success message
            return redirect('some_success_url')  # Replace with appropriate URL

    # Retrieve existing records associated with the professor
    capacities = Capacity.objects.filter(Professor=professor).order_by('-Year__Year')
    frees = Free.objects.filter(Professor=professor).order_by('-Year__Year')
    capacity_sections = CapacitySection.objects.filter(Professor=professor).order_by('-Year__Year')

    # Extract unique years from all three querysets
    years = sorted(set(chain(
        capacities.values_list('Year__Year', flat=True),
        frees.values_list('Year__Year', flat=True),
        capacity_sections.values_list('Year__Year', flat=True)
    )))

    context = {
        'capacity_form': capacity_form,
        'free_form': free_form,
        'capacity_section_form': capacity_section_form,
        'professor': professor,
        'capacities': capacities,
        'frees': frees,
        'capacity_sections': capacity_sections,
        'years': years,
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
            messages.success(request, 'Capacitat correctament creada.')
            return redirect('capacityprofessor_edit', idProfessor=idProfessor)
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
            messages.success(request, 'Capacitat correctament editada.')
            return redirect('capacityprofessor_edit', idProfessor=idProfessor)
    else:
        form = CapacityForm(instance=capacity)

    return render(request, 'professor_capacity/professor_capacity_form.html', {'form': form, 'professor': capacity.Professor, 'year': capacity.Year})

def delete_capacity(request, idCapacity):
    capacity = get_object_or_404(Capacity, pk=idCapacity)
    idProfessor = capacity.Professor.idProfessor  
    try:
        capacity.delete()
        messages.success(request, 'Capacitat correctament eliminada.')
    except Exception as e:
        messages.error(request, f"Error: No s'ha pogut eliminar la capacitat ({e}).")

    return redirect('capacityprofessor_edit', idProfessor=idProfessor)

#FREE
# Create a new Free entry
def create_free(request, idProfessor):
    professor = get_object_or_404(Professor, pk=idProfessor)

    if request.method == 'POST':
        form = FreeForm(request.POST,professor=professor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Punts Lliures correctament creats.')
            return redirect('capacityprofessor_edit', idProfessor=idProfessor)
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
            messages.success(request, 'Punts Lliures correctament editats.')
            return redirect('capacityprofessor_edit', idProfessor=idProfessor)
    else:
        form = FreeForm(instance=free)

    return render(request, 'professor_capacity/professor_capacity_form.html', {'form': form, 'professor': free.Professor, 'year': free.Year})

def delete_free(request, idFree):
    free = get_object_or_404(Free, pk=idFree)
    idProfessor = free.Professor.idProfessor  
    try:
        free.delete()
        messages.success(request, 'Punts Lliures correctament eliminats.')
    except Exception as e:
        messages.error(request, f"Error: No s'ha pogut eliminar els punts lliures ({e}).")

    return redirect('capacityprofessor_edit', idProfessor=idProfessor)

#CAPACITY SECTION
# Create a new Capacity section entry
def create_capacity_section(request, idProfessor):
    professor = get_object_or_404(Professor, pk=idProfessor)

    if request.method == 'POST':
        form = CapacitySectionForm(request.POST,professor=professor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Capacitat en la Secció correctament creada.')
            return redirect('capacityprofessor_edit', idProfessor=idProfessor)
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
            messages.success(request, 'Capacitat en la Secció correctament editada.')
            return redirect('capacityprofessor_edit', idProfessor=idProfessor)
    else:
        form = CapacitySectionForm(instance=capsection,professor=capsection.Professor)

    return render(request, 'professor_capacity/professor_capacity_form.html', {'form': form, 'professor': capsection.Professor, 'year': capsection.Year})

def delete_capacity_section(request, idCapacitySection):
    capsection = get_object_or_404(CapacitySection, pk=idCapacitySection)
    idProfessor = capsection.Professor.idProfessor  
    try:
        capsection.delete()
        messages.success(request, 'Capacitat en la secció correctament eliminada.')
    except Exception as e:
        messages.error(request, f"Error: No s'ha pogut eliminar la capacitat ({e}).")

    return redirect('capacityprofessor_edit', idProfessor=idProfessor)

#SECTIONS
def capacitysection_list(request):
    pass

def capacitysection_create_edit(request,idSection=None):
    pass
