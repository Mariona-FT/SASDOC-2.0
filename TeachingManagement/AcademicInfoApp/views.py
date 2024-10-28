from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from .models import Field,Section,School,Degree,Course,TypeProfessor,Language,Year
from .forms import FieldForm,SectionForm,SchoolForm,DegreeForm,CourseForm,TypeProfessorForm,LanguageForm,YearForm

# Create your views here.

### FIELD ###

## Field list to manage - listing and actions of edit, delete and add field
def field_list(request):
    fields = Field.objects.all()
    deleting = None

    # FINAL DELETE
    if request.method == "POST" and 'confirm_delete' in request.POST:
        field_id = request.POST.get('confirm_delete') # id passed in url
        try:
            field = Field.objects.get(pk=field_id)
            field_name = field.NameField  # Store the name for the message
            field.delete()
            messages.success(request, f"El camp {field_name} s'ha eliminat correctament.")
            return redirect('field_list') 
        except Field.DoesNotExist:
            messages.error(request, "Error: El camp no existeix.")

    # ACTION OF INITIAL DELETE
    if 'confirm_delete' in request.GET:
        field_id = request.GET.get('confirm_delete')
        deleting = field_id  # Get id field to delete

    return render(request, 'field_list_actions.html', {
        'fields': fields,
        'deleting': deleting,
    })

#Function to create or edit a field - depends if is passed a idField 
def field_create_edit(request, idField=None):
    if idField:
        # If idField is passed, we are editing an existing field
        field = get_object_or_404(Field, pk=idField)
        if request.method == 'POST':
            form = FieldForm(request.POST, instance=field)
            if form.is_valid():
                form.save()
                messages.success(request, f'El camp "{field.NameField}" s\'ha actualitzat correctament.')
                return redirect('field_list')
        else:
            form = FieldForm(instance=field)
    else:
        # No idField, we are creating a new field
        if request.method == 'POST':
            form = FieldForm(request.POST)
            if form.is_valid():
                new_field = form.save()
                messages.success(request, f'El camp "{new_field.NameField}" s\'ha afegit correctament.')
                return redirect('field_list')
        else:
            form = FieldForm()

    return render(request, 'field_form.html', {'form': form})


### SECTION ###

## Section list to manage - listing and actions of edit, delete and add section
def section_list(request):
    sections = Section.objects.all()
    deleting = None

    # FINAL DELETE
    if request.method == "POST" and 'confirm_delete' in request.POST:
        section_id = request.POST.get('confirm_delete') # id passed in url
        try:
            section = Section.objects.get(pk=section_id)
            section_name = section.NameSection  # Store the name for the message
            section.delete()
            messages.success(request, f"La secció {section_name} s'ha eliminat correctament.")
            return redirect('section_list') 
        except Section.DoesNotExist:
            messages.error(request, "Error: La secció no existeix.")
    
    # ACTION OF INITIAL DELETE
    if 'confirm_delete' in request.GET:
        section_id = request.GET.get('confirm_delete')
        deleting = section_id # Get id section to delete

    return render(request, 'section_list_actions.html', {
        'sections': sections,
        'deleting': deleting,
    })

#Function to create or edit a section - depends if is passed a idSection 
def sections_create_edit(request,idSection=None):
    if idSection:
        # If idSection is passed, we are editing an existing section
        section = get_object_or_404(Section, pk=idSection)
        if request.method == 'POST':
            form = SectionForm(request.POST, instance=section)
            if form.is_valid():
                form.save()
                messages.success(request, f'La secció {section.NameSection} s\'ha actualitzat correctament.')
                return redirect('section_list')
        else:
            form = SectionForm(instance=section)
    else:
        # No idSection, we are creating a new section
        if request.method == 'POST':
            form = SectionForm(request.POST)
            if form.is_valid():
                new_section = form.save()
                messages.success(request, f'La secció {new_section.NameSection} s\'ha afegit correctament.')
                return redirect('section_list')
        else:
            form = SectionForm()

    return render(request, 'section_form.html', {'form': form})


### SCHOOLS ###

## Schools list to manage - listing and actions of edit, delete and add schools
def school_list(request):
    schools = School.objects.all()
    deleting = None
   
    if request.method == "POST" and 'confirm_delete' in request.POST:       
        # FINAL DELETE
        school_id = request.POST.get('confirm_delete') # id passed in url
        try:
            school = School.objects.get(pk=school_id)
            school_name = school.NameSchool  # Store the name for the message
            school.delete()
            messages.success(request, f"L'escola {school_name} s'ha eliminat correctament.")
            return redirect('school_list') 
        except School.DoesNotExist:
            messages.error(request, "Error: L'escola no existeix.")
    
    # ACTION OF INITIAL DELETE
    if 'confirm_delete' in request.GET:
        school_id = request.GET.get('confirm_delete')
        deleting = school_id  # Get id school to delete
    
    return render(request, 'school_list_actions.html', {
        'schools': schools,
        'deleting': deleting,
    })

#Function to create or edit a school - depends if is passed a idschool 
def school_create_edit(request,idSchool=None):
    if idSchool:
        # If idschool is passed, we are editing an existing school
        school = get_object_or_404(School, pk=idSchool)
        if request.method == 'POST':
            form = SchoolForm(request.POST, instance=school)
            if form.is_valid():
                form.save()
                messages.success(request, f"L'Escola {school.NameSchool} s\'ha actualitzat correctament.")
                return redirect('school_list')
        else:
            form = SchoolForm(instance=school)
    else:
        # No idSchool, we are creating a new school
        if request.method == 'POST':
            form = SchoolForm(request.POST)
            if form.is_valid():
                new_school = form.save()
                messages.success(request, f"L'escola {new_school.NameSchool} s\'ha afegit correctament.")
                return redirect('school_list')
        else:
            form = SchoolForm()
    return render(request, 'school_form.html', {'form': form})
    
### DEGREE ###

## Degree list to manage - listing and actions of edit, delete and add degree
def degree_list(request):
    degrees = Degree.objects.all()
    deleting = None
   
    if request.method == "POST" and 'confirm_delete' in request.POST:
       # FINAL DELETE
        degree_id = request.POST.get('confirm_delete') # id passed in url
        try:
            degree = Degree.objects.get(pk=degree_id)
            degree_name = degree.NameDegree  # Store the name for the message
            degree.delete()
            messages.success(request, f"La Titulació {degree_name} s'ha eliminat correctament.")
            return redirect('degree_list') 
        except Degree.DoesNotExist:
            messages.error(request, "Error: La Titulació no existeix.")
    
    # ACTION OF INITIAL DELETE
    if 'confirm_delete' in request.GET:
        degree_id = request.GET.get('confirm_delete')
        deleting = degree_id  # Only pass the ID for now
    
    return render(request, 'degree_list_actions.html', {
        'degrees': degrees,
        'deleting': deleting,
    })

#Function to create or edit a degree - depends if is passed a idegree 
def degree_create_edit(request,idDegree=None):
    if idDegree:
        # If idDegree is passed, we are editing an existing degree
        degree = get_object_or_404(Degree, pk=idDegree)
        if request.method == 'POST':
            form = DegreeForm(request.POST, instance=degree)
            if form.is_valid():
                form.save()
                messages.success(request, f"La Titulació {degree.NameDegree} s\'ha actualitzat correctament.")
                return redirect('degree_list')
        else:
            form = DegreeForm(instance=degree)
    else:
        # No idDegree, we are creating a new degree
        if request.method == 'POST':
            form = DegreeForm(request.POST)
            if form.is_valid():
                new_degree = form.save()
                messages.success(request, f"La Titulació {new_degree.NameDegree} s\'ha afegit correctament.")
                return redirect('degree_list')
        else:
            form = DegreeForm()
    return render(request, 'degree_form.html', {'form': form})


### COURSES ###

## Course list to manage - listing and actions of edit, delete and add course
def course_list(request):
    courses = Course.objects.all()
    deleting = None
   
    if request.method == "POST" and 'confirm_delete' in request.POST:
       # FINAL DELETE
        course_id = request.POST.get('confirm_delete') # id passed in url
        try:
            course = Course.objects.get(pk=course_id)
            course_name = course.NameCourse  # Store the name for the message
            course.delete()
            messages.success(request, f"El Curs {course_name} s'ha eliminat correctament.")
            return redirect('course_list') 
        except Course.DoesNotExist:
            messages.error(request, "Error: El Curs no existeix.")
    
    # ACTION OF INITIAL DELETE
    if 'confirm_delete' in request.GET:
        course_id = request.GET.get('confirm_delete')
        deleting = course_id  # Only pass the ID for now

    return render(request, 'course_list_actions.html', {
        'courses': courses,
        'deleting': deleting,
    })


#Function to create or edit a course - depends if is passed a idCourse 
def course_create_edit(request,idCourse=None):
    if idCourse:
        # If idCourse is passed, we are editing an existing courses
        course = get_object_or_404(Course, pk=idCourse)
        if request.method == 'POST':
            form = CourseForm(request.POST, instance=course)
            if form.is_valid():
                form.save()
                messages.success(request, f"El curs {course.NameCourse} s\'ha actualitzat correctament.")
                return redirect('course_list')
        else:
            form = CourseForm(instance=course)
    else:
        # No idCourse, we are creating a new course
        if request.method == 'POST':
            form = CourseForm(request.POST)
            if form.is_valid():
                new_course = form.save()
                messages.success(request, f"El curs {new_course.NameCourse} s\'ha afegit correctament.")
                return redirect('course_list')
        else:
            form = CourseForm()
    return render(request, 'course_form.html', {'form': form})

########################################################################################################


### TYPE PROFESSOR ###
def type_professor_crud(request):
    type_professors = TypeProfessor.objects.all()
    form = TypeProfessorForm()
    deleting = None

    if request.method == "POST":
        # Handle delete confirmation
        if 'confirm_delete' in request.POST:
            type_professor_id = request.POST.get('confirm_delete')
            type_professor = get_object_or_404(TypeProfessor, pk=type_professor_id)
            type_professor_name = type_professor.Name
            type_professor.delete()
            messages.success(request, f"El tipus de professor {type_professor_name} s'ha eliminat correctament.")
            return redirect('type_professor_crud')

        # Handle update
        if 'idTypeProfessor' in request.POST:
            type_professor_id = request.POST.get('idTypeProfessor')
            type_professor = get_object_or_404(TypeProfessor, pk=type_professor_id)
            form = TypeProfessorForm(request.POST, instance=type_professor)
            if form.is_valid():
                form.save()
                messages.success(request, f"El tipus de professor {type_professor.Name} s'ha actualitzat correctament.")
                return redirect('type_professor_crud')

        # Handle create
        else:
            form = TypeProfessorForm(request.POST)
            if form.is_valid():
                type_professor = form.save()
                messages.success(request, f"El tipus de professor {type_professor.Name} s'ha creat correctament.")
                return redirect('type_professor_crud')

    # Handle edit
    if 'edit' in request.GET:
        type_professor_id = request.GET.get('edit')
        type_professor = get_object_or_404(TypeProfessor, pk=type_professor_id)
        form = TypeProfessorForm(instance=type_professor)

    # Handle initial delete confirmation
    if 'confirm_delete' in request.GET:
        type_professor_id = request.GET.get('confirm_delete')
        deleting = get_object_or_404(TypeProfessor, pk=type_professor_id)

    return render(request, 'type_professor_crud.html', {
        'form': form,
        'type_professors': type_professors,
        'deleting': deleting,
    })


### LANGUAGES ###
def language_crud(request):
    languages = Language.objects.all()
    form = LanguageForm()
    deleting = None

    if request.method == "POST":
        # Handle delete confirmation
        if 'confirm_delete' in request.POST:
            language_id = request.POST.get('confirm_delete')
            language = get_object_or_404(Language, pk=language_id)
            language_name = language.Language
            language.delete()
            messages.success(request, f"La llengua {language_name} s'ha eliminat correctament.")
            return redirect('language_crud')

        # Handle update
        if 'idLanguage' in request.POST:
            language_id = request.POST.get('idLanguage')
            language = get_object_or_404(Language, pk=language_id)
            form = LanguageForm(request.POST, instance=language)
            if form.is_valid():
                form.save()
                messages.success(request, f"La llengua {language.Language} s'ha actualitzat correctament.")
                return redirect('language_crud')

        # Handle create
        else:
            form = LanguageForm(request.POST)
            if form.is_valid():
                language = form.save()
                messages.success(request, f"La llengua {language.Language} s'ha creat correctament.")
                return redirect('language_crud')

    # Handle edit
    if 'edit' in request.GET:
        language_id = request.GET.get('edit')
        language = get_object_or_404(Language, pk=language_id)
        form = LanguageForm(instance=language)

    # Handle initial delete confirmation
    if 'confirm_delete' in request.GET:
        laguage_id = request.GET.get('confirm_delete')
        deleting = get_object_or_404(Language, pk=language_id)

    return render(request, 'language_crud.html', {
        'form': form,
        'languages': languages,
        'deleting': deleting,
    })

### YEAR ###
def year_crud(request):
    years = Year.objects.all().order_by('-Year')
    form = YearForm()
    deleting = None

    if request.method == "POST":
        # Handle delete confirmation
        if 'confirm_delete' in request.POST:
            year_id = request.POST.get('confirm_delete')
            year = get_object_or_404(Year, pk=year_id)
            year_value = year.Year
            year.delete()
            messages.success(request, f"L'any {year_value} s'ha eliminat correctament.")
            return redirect('year_crud')

        # Handle update
        if 'idYear' in request.POST:
            year_id = request.POST.get('idYear')
            # Get the existing year object
            original_year = get_object_or_404(Year, pk=year_id)
            form = YearForm(request.POST, instance=original_year)

            if form.is_valid():
                # Update the existing year without deleting
                updated_year = form.save()
                messages.success(request, f"L'any {updated_year.Year} s'ha actualitzat correctament.")
                return redirect('year_crud')

        # Handle create
        else:
            form = YearForm(request.POST)
            if form.is_valid():
                year = form.save()
                messages.success(request, f"L'any {year.Year} s'ha creat correctament.")
                return redirect('year_crud')

    # Handle edit
    if 'edit' in request.GET:
        year_id = request.GET.get('edit')
        year = get_object_or_404(Year, pk=year_id)
        form = YearForm(instance=year)

    # Handle initial delete confirmation
    if 'confirm_delete' in request.GET:
        year_id = request.GET.get('confirm_delete')
        deleting = get_object_or_404(Year, pk=year_id)

    return render(request, 'year_crud.html', {
        'form': form,
        'years': years,
        'deleting': deleting,
    })