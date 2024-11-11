from django.shortcuts import render, redirect,get_object_or_404
from .forms import CapacityForm, FreeForm, CapacitySectionForm
from .models import Professor, Capacity, Free, CapacitySection
from UsersApp.models import Professor
from AcademicInfoApp.models import Section,Year
from django.contrib import messages
from itertools import chain

# Create your views here.

#PROFESSORS
def capacityprofessor_list(request):
    # Get all years for capacity selection
    years = Capacity.objects.values_list('Year__Year', flat=True).distinct()
    selected_year = request.GET.get('idYear')
    
    # Get all professors ordered by family name
    professors = Professor.objects.all().order_by('family_name')
    all_sections = Section.objects.all()
    professor_data = []

    for professor in professors:
        # Filter capacities by professor and selected year
        capacities = Capacity.objects.filter(Professor=professor, Year__Year=selected_year).order_by('Year__Year') if selected_year else None
        free_points = Free.objects.filter(Professor=professor).first()
        
        # Initialize section points list as tuples (section_name, points)
        section_points = [(section.NameSection, 0) for section in all_sections]
        
        # Update section points from CapacitySection entries
        for section_entry in CapacitySection.objects.filter(Professor=professor, Year__Year=selected_year):
            section_name = section_entry.Section.NameSection
            section_points = [(name, section_entry.Points if name == section_name else points) for name, points in section_points]
        
        # Set capacity_points and year based on the selected year’s capacities
        if capacities:
            capacity_points = capacities[0].Points
            year = capacities[0].Year.Year
        else:
            capacity_points = 0
            year = "NA"
        
        # Calculate total section points sum
        section_points_sum = sum(points for _, points in section_points)
        
        # Determine background color
        if not selected_year:
            background_color = '#d9d9d9'
        elif capacity_points + (free_points.PointsFree if free_points else 0) == section_points_sum:
            background_color = '#ffe6e6'
        else:
            background_color = '#e6ffea'
        
        # Append each professor's data
        professor_data.append({
            'professor': professor,
            'capacity_points': capacity_points,
            'year': year,
            'free_points': free_points.PointsFree if free_points else 0,
            'section_points': section_points,
            'background_color': background_color,
        })

    return render(request, 'professor_capacity/capacityprofessor_list_actions.html', {
        'professor_data': professor_data,
        'all_sections': all_sections,
        'years': years,
        'selected_year': selected_year,
    })

def capacityprofessor_list_for_year(request,idYear):
    pass

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
