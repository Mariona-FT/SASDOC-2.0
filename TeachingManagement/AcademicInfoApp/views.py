from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from .models import Field,Section,School,Degree
from .forms import FieldForm,SectionForm,SchoolForm,DegreeForm

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

### SCHOOLS ###
def school_crud(request):
    schools = School.objects.all()
    form = SchoolForm()  # Initialize the form
    deleting = None

    if request.method == "POST":
        # FINAL DELETE
        if 'confirm_delete' in request.POST:
            school_id = request.POST.get('confirm_delete')  # id passed in request
            print("Intentant eliminar l'escola amb ID:", school_id)  
            try:
                school = School.objects.get(pk=school_id)
                school_name = school.NameSchool  # Store the name for the message
                school.delete()
                messages.success(request, f"{school_name} s'ha eliminat correctament.")
                return redirect('school_crud') 
            except School.DoesNotExist:
                messages.error(request, "Error: L'escola no existeix.")
                print("Error: L'escola amb ID", school_id, "no existeix.")  

        # UPDATE
        if 'idSchool' in request.POST:  
            school_id = request.POST.get('idSchool')
            print("Intentant actualitzar l'escola amb ID:", school_id)  
            school = get_object_or_404(School, pk=school_id)  # Check if school exists
            form = SchoolForm(request.POST, instance=school) 
            if form.is_valid():  # Check if form is valid
                form.save()
                messages.success(request, f"{school.NameSchool} s'ha actualitzat correctament.")
                return redirect('school_crud') 
            else:
                print("Errors en el formulari d'actualització:", form.errors)  
                messages.error(request, "Error en actualitzar l'escola. Si us plau, revisa els camps.")

        # CREATE
        else:
            form = SchoolForm(request.POST)  # Initialize form with POST data
            print("Intentant crear una nova escola:", request.POST)  
            if form.is_valid():  # Check if form is valid
                school = form.save()
                messages.success(request, f"{school.NameSchool} s'ha creat correctament.")
                return redirect('school_crud')  
            else:
                print("Errors en el formulari de creació:", form.errors)  
                messages.error(request, "Error en crear l'escola. Si us plau, revisa els camps.")

    # UPDATE FORM
    if 'edit' in request.GET:
        school_id = request.GET.get('edit')
        print("Intentant editar l'escola amb ID:", school_id)  
        school = get_object_or_404(School, pk=school_id)
        form = SchoolForm(instance=school)
    
    # ACTION OF INITIAL DELETE
    if 'confirm_delete' in request.GET:
        school_id = request.GET.get('confirm_delete')
        deleting = get_object_or_404(School, pk=school_id)  # Get school to delete

    return render(request, 'school_crud.html', {
        'form': form,
        'schools': schools,
        'deleting': deleting,
    })
    

def degree_crud(request):
    degrees = Degree.objects.all()
    form = DegreeForm()  # Initialize the form
    deleting = None

    if request.method == "POST":
        # FINAL DELETE
        if 'confirm_delete' in request.POST:
            degree_id = request.POST.get('confirm_delete')
            print("Intentant eliminar el grau amb ID:", degree_id)
            try:
                degree = Degree.objects.get(pk=degree_id)
                degree_name = degree.NameDegree  # Store the name for the message
                degree.delete()
                messages.success(request, f"{degree_name} s'ha eliminat correctament.")
                return redirect('degree_crud')
            except Degree.DoesNotExist:
                messages.error(request, "Error: El grau no existeix.")
                print("Error: El grau amb ID", degree_id, "no existeix.")

        # UPDATE
        if 'idDegree' in request.POST:
            degree_id = request.POST.get('idDegree')
            print("Intentant actualitzar el grau amb ID:", degree_id)
            degree = get_object_or_404(Degree, pk=degree_id)  # Check if degree exists
            form = DegreeForm(request.POST, instance=degree)
            if form.is_valid():  # Check if form is valid
                form.save()
                messages.success(request, f"{degree.NameDegree} s'ha actualitzat correctament.")
                return redirect('degree_crud')
            else:
                print("Errors en el formulari d'actualització:", form.errors)
                messages.error(request, "Error en actualitzar el grau. Si us plau, revisa els camps.")

        # CREATE
        else:
            form = DegreeForm(request.POST)  # Initialize form with POST data
            print("Intentant crear un nou grau:", request.POST)
            if form.is_valid():  # Check if form is valid
                degree = form.save()
                messages.success(request, f"{degree.NameDegree} s'ha creat correctament.")
                return redirect('degree_crud')
            else:
                print("Errors en el formulari de creació:", form.errors)
                messages.error(request, "Error en crear el grau. Si us plau, revisa els camps.")

    # UPDATE FORM
    if 'edit' in request.GET:
        degree_id = request.GET.get('edit')
        print("Intentant editar el grau amb ID:", degree_id)
        degree = get_object_or_404(Degree, pk=degree_id)
        form = DegreeForm(instance=degree)

    # ACTION OF INITIAL DELETE
    if 'confirm_delete' in request.GET:
        degree_id = request.GET.get('confirm_delete')
        deleting = get_object_or_404(Degree, pk=degree_id)  # Get degree to delete

    return render(request, 'degree_crud.html', {
        'form': form,
        'degrees': degrees,
        'deleting': deleting,
    })

def course_crud(request):
    pass