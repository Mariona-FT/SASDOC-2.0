from django.shortcuts import render, redirect
from .forms import CapacityFreeSectionForm
from .models import Professor, Capacity, Free, CapacitySection
from UsersApp.models import Professor
from AcademicInfoApp.models import Section
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

def capacityprofessor_create_edit(request,idProfessor=None):
    if request.method == 'POST':
        form = CapacityFreeSectionForm(request.POST)
        if form.is_valid():
            form.save()  # Save all instances
            return redirect('')  # Redirect to a success page or the same page with a success message
    else:
        form = CapacityFreeSectionForm()

    return render(request, 'capacityprofessor_form.html', {'form': form})


#SECTIONS
def capacitysection_list(request):
    pass

def capacitysection_create_edit(request,idSection=None):
    pass
