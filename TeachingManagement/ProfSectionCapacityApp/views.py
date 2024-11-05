from django.shortcuts import render, redirect,get_object_or_404
from .forms import CapacityForm, FreeForm, CapacitySectionForm
from .models import Professor, Capacity, Free, CapacitySection
from UsersApp.models import Professor
from AcademicInfoApp.models import Section,Year
from django.contrib import messages

# Create your views here.

#PROFESSORS
def capacityprofessor_list(request):
    professors = Professor.objects.all().order_by('family_name')
    all_sections = Section.objects.all()  
    professor_data = []
    deleting = None

    for professor in professors:
        # Retrieve capacity points
        capacity_points = Capacity.objects.filter(Professor=professor).first()
        free_points = Free.objects.filter(Professor=professor).first()

        # Retrieve and sum up section points
        section_points = {section.NameSection: 0 for section in all_sections}
        for section_entry in CapacitySection.objects.filter(Professor=professor):
            section_name = section_entry.Section.NameSection
            section_points[section_name] = section_entry.Points

        # Append data for each professor
        professor_data.append({
            'professor': professor,
            'capacity_points': capacity_points.Points if capacity_points else 0,
            'free_points': free_points.PointsFree if free_points else 0,
            'section_points': section_points,
        })

    if request.method == "POST" and 'confirm_delete' in request.POST:
        # FINAL DELETE
        
        professor_id = request.POST.get('confirm_delete')
        print(f"Attempting to delete professor with ID: {professor_id}")  # Print the ID being passed

        try:
            professor = Professor.objects.get(idProfessor=professor_id)
            professor_name = f"{professor.name} {professor.family_name}"

            user = professor.user
            if user:
                print(f"Deleting associated CustomUser with ID: {user}")  # Print the user ID being deleted
                user.delete()  # Delete the user

            professor.delete()
            messages.success(request, f"El professor {professor_name} s'ha eliminat correctament.")
            return redirect('usersapp:professor_list')
        except Professor.DoesNotExist:
            messages.error(request,"Error: El professor no existeix i no s'ha pogut borrar.")
            print(f"Professor with ID {professor_id} does not exist.")  # Print error information

    # Handle initial delete confirmation
    if 'confirm_delete' in request.GET:
        professor_id = request.GET.get('confirm_delete')
        deleting = professor_id
        print("Delete confirmation for professor ID:", deleting)  # Print the ID being confirmed for deletion

    return render(request, 'capacityprofessor_list_actions.html', {
        'professor_data': professor_data,
        'all_sections':all_sections,
        'deleting': deleting,
    })

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

    context = {
        'capacity_form': capacity_form,
        'free_form': free_form,
        'capacity_section_form': capacity_section_form,
        'professor': professor,
        'capacities': capacities,
        'frees': frees,
        'capacity_sections': capacity_sections,
    }
    return render(request, 'capacityprofessor_form.html', context)

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

    return render(request, 'capacity_form.html', {'form': form, 'professor': professor})

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

    return render(request, 'capacity_form.html', {'form': form, 'professor': capacity.Professor, 'year': capacity.Year})

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

    return render(request, 'free_form.html', {'form': form, 'professor': professor})

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

    return render(request, 'capacity_form.html', {'form': form, 'professor': free.Professor, 'year': free.Year})

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

    return render(request, 'capacity_section_form.html', {'form': form, 'professor': professor})

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

    return render(request, 'capacity_form.html', {'form': form, 'professor': capsection.Professor, 'year': capsection.Year})

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
