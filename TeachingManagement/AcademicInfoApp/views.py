from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from .models import Field,Section
from .forms import FieldForm,SectionForm

# Create your views here.

### FIELD ###
def field_crud(request):
    fields = Field.objects.all()
    form = FieldForm()  # Initialize the form
    deleting = None

    if request.method == "POST":

       # FINAL DELETE
        if 'confirm_delete' in request.POST:
            field_id = request.POST.get('confirm_delete') # id passed in url
            print("Intentant eliminar el camp amb ID:", field_id)  
            try:
                field = Field.objects.get(pk=field_id)
                field_name = field.NameField  # Store the name for the message
                field.delete()
                messages.success(request, f"{field_name} s'ha eliminat correctament.")
                return redirect('field_crud') 
            except Field.DoesNotExist:
                messages.error(request, "Error: El camp no existeix.")
                print("Error: El camp amb ID", field_id, "no existeix.")  

        # UPDATE
        if 'idField' in request.POST:  
            field_id = request.POST.get('idField')
            print("Intentant actualitzar el camp amb ID:", field_id)  
            field = get_object_or_404(Field, pk=field_id) #Check if field is in bd
            form = FieldForm(request.POST, instance=field) 
            if form.is_valid(): #Check form correct
                form.save()
                messages.success(request, f"{field.NameField} s'ha actualitzat correctament.")
                return redirect('field_crud') 
            else:
                print("Errors en el formulari d'actualització:", form.errors)  
                messages.error(request, "Error en actualitzar el camp. Si us plau, revisa els camps.")

        # CREATE
        else:
            form = FieldForm(request.POST) #enter all the info of the form
            print("Intentant crear un nou camp:", request.POST)  
            if form.is_valid(): #Check form correct
                field = form.save()
                messages.success(request, f"{field.NameField} s'ha creat correctament.")
                return redirect('field_crud')  
            else:
                print("Errors en el formulari de creació:", form.errors)  
                messages.error(request, "Error en crear el camp. Si us plau, revisa els camps.")

    # UPDATE FORM
    if 'edit' in request.GET:
        field_id = request.GET.get('edit')
        print("Intentant editar el camp amb ID:", field_id)  
        field = get_object_or_404(Field, pk=field_id)
        form = FieldForm(instance=field)
    
    # ACTION OF INITIAL DELETE
    if 'confirm_delete' in request.GET:
        field_id = request.GET.get('confirm_delete')
        deleting = get_object_or_404(Field, pk=field_id)  # Get id field to delete

    return render(request, 'field_crud.html', {
        'form': form,
        'fields': fields,
        'deleting': deleting,
    })


### SECTION ###
def section_crud(request):
    sections = Section.objects.all()
    form = SectionForm()  # Initialize the form
    deleting = None

    if request.method == "POST":
        # FINAL DELETE
        if 'confirm_delete' in request.POST:
            section_id = request.POST.get('confirm_delete')  # id passed in request
            print("Intentant eliminar la secció amb ID:", section_id)  
            try:
                section = Section.objects.get(pk=section_id)
                section_name = section.NameSection  # Store the name for the message
                section.delete()
                messages.success(request, f"{section_name} s'ha eliminat correctament.")
                return redirect('section_crud') 
            except Section.DoesNotExist:
                messages.error(request, "Error: La secció no existeix.")
                print("Error: La secció amb ID", section_id, "no existeix.")  

        # UPDATE
        if 'idSection' in request.POST:  
            section_id = request.POST.get('idSection')
            print("Intentant actualitzar la secció amb ID:", section_id)  
            section = get_object_or_404(Section, pk=section_id)  # Check if section exists
            form = SectionForm(request.POST, instance=section) 
            if form.is_valid():  # Check if form is valid
                form.save()
                messages.success(request, f"{section.NameSection} s'ha actualitzat correctament.")
                return redirect('section_crud') 
            else:
                print("Errors en el formulari d'actualització:", form.errors)  
                messages.error(request, "Error en actualitzar la secció. Si us plau, revisa els camps.")

        # CREATE
        else:
            form = SectionForm(request.POST)  # Initialize form with POST data
            print("Intentant crear una nova secció:", request.POST)  
            if form.is_valid():  # Check if form is valid
                section = form.save()
                messages.success(request, f"{section.NameSection} s'ha creat correctament.")
                return redirect('section_crud')  
            else:
                print("Errors en el formulari de creació:", form.errors)  
                messages.error(request, "Error en crear la secció. Si us plau, revisa els camps.")

    # UPDATE FORM
    if 'edit' in request.GET:
        section_id = request.GET.get('edit')
        print("Intentant editar la secció amb ID:", section_id)  
        section = get_object_or_404(Section, pk=section_id)
        form = SectionForm(instance=section)
    
    # ACTION OF INITIAL DELETE
    if 'confirm_delete' in request.GET:
        section_id = request.GET.get('confirm_delete')
        deleting = get_object_or_404(Section, pk=section_id)  # Get section to delete

    return render(request, 'section_crud.html', {
        'form': form,
        'sections': sections,
        'deleting': deleting,
    })

def school_crud(request):
    pass

def degree_crud(request):
    pass

def course_crud(request):
    pass