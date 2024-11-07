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
    sections = Section.objects.all().order_by('LetterSection')
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
    schools = School.objects.all().order_by('CodeSchool')
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
    degrees = Degree.objects.all().order_by('CodeDegree')
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
        deleting = degree_id  # Only pass the ID
    
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
    courses = Course.objects.all().order_by('CodeCourse')
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
        deleting = course_id  # Only pass the ID

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

### TYPE PROFESSOR ###

## typeprofessor list to manage - listing and actions of edit, delete and add typeprofessor
def typeprofessor_list(request):
    typeprofessors = TypeProfessor.objects.all()
    deleting = None
   
    if request.method == "POST" and 'confirm_delete' in request.POST:
       # FINAL DELETE
        typeprofessor_id = request.POST.get('confirm_delete') # id passed in url
        try:
            typeprofessor = TypeProfessor.objects.get(pk=typeprofessor_id)
            typeprofessor_name = typeprofessor.NameContract  # Store the name for the message
            typeprofessor.delete()
            messages.success(request, f"El tipus de Professor {typeprofessor_name} s'ha eliminat correctament.")
            return redirect('typeprofessor_list') 
        except TypeProfessor.DoesNotExist:
            messages.error(request, "Error: El tipus de professor no existeix.")
    
    # ACTION OF INITIAL DELETE
    if 'confirm_delete' in request.GET:
        typeprofessor_id = request.GET.get('confirm_delete')
        deleting = typeprofessor_id  # Only pass the ID

    return render(request, 'typeprofessor_list_actions.html', {
        'type_professors': typeprofessors,
        'deleting': deleting,
    })


#Function to create or edit a typeprofessor - depends if is passed a idTypeProfessor 
def typeprofessor_create_edit(request,idTypeProfessor=None):
    if idTypeProfessor:
        # If idTypeProfessor is passed, we are editing an existing TypeProfessor
        typeprofessor = get_object_or_404(TypeProfessor, pk=idTypeProfessor)
        if request.method == 'POST':
            form = TypeProfessorForm(request.POST, instance=typeprofessor)
            if form.is_valid():
                form.save()
                messages.success(request, f"El tipus de professor {typeprofessor.NameContract} s\'ha actualitzat correctament.")
                return redirect('typeprofessor_list')
        else:
            form = TypeProfessorForm(instance=typeprofessor)
    else:
        # No idTypeProfessor, we are creating a new typeprofessor
        if request.method == 'POST':
            form = TypeProfessorForm(request.POST)
            if form.is_valid():
                new_typeprofessor = form.save()
                messages.success(request, f"El tipus de professor {new_typeprofessor.NameContract} s\'ha afegit correctament.")
                return redirect('typeprofessor_list')
        else:
            form = TypeProfessorForm()
    return render(request, 'typeprofessor_form.html', {'form': form})

### LANGUAGES ###

## language list to manage - listing and actions of edit, delete and add language
def language_list(request):
    languages = Language.objects.all()
    deleting = None
   
    if request.method == "POST" and 'confirm_delete' in request.POST:
       # FINAL DELETE
        language_id = request.POST.get('confirm_delete') # id passed in url
        try:
            language = Language.objects.get(pk=language_id)
            language_name = language.Language  # Store the name for the message
            language.delete()
            messages.success(request, f"L'idioma {language_name} s'ha eliminat correctament.")
            return redirect('language_list') 
        except Language.DoesNotExist:
            messages.error(request, "Error: L'idioma no existeix.")
    
    # ACTION OF INITIAL DELETE
    if 'confirm_delete' in request.GET:
        language_id = request.GET.get('confirm_delete')
        deleting = language_id  # Only pass the ID

    return render(request, 'language_list_actions.html', {
        'languages': languages,
        'deleting': deleting,
    })

#Function to create or edit a language - depends if is passed a idLanguage 
def language_create_edit(request,idLanguage=None):
    if idLanguage:
        # If idLanguage is passed, we are editing an existing language
        language = get_object_or_404(Language, pk=idLanguage)
        if request.method == 'POST':
            form = LanguageForm(request.POST, instance=language)
            if form.is_valid():
                form.save()
                messages.success(request, f"L'idioma {language.Language} s\'ha actualitzat correctament.")
                return redirect('language_list')
        else:
            form = LanguageForm(instance=language)
    else:
        # No idLanguage, we are creating a new language
        if request.method == 'POST':
            form = LanguageForm(request.POST)
            if form.is_valid():
                new_language = form.save()
                messages.success(request, f"L'idioma {new_language.Language} s\'ha afegit correctament.")
                return redirect('language_list')
        else:
            form = LanguageForm()
    return render(request, 'language_form.html', {'form': form})


### YEAR ###

## year list to manage - listing and actions of edit, delete and add year
def year_list(request):
    years = Year.objects.all().order_by('Year')
    deleting = None
   
    if request.method == "POST" and 'confirm_delete' in request.POST:
       # FINAL DELETE
        year_id = request.POST.get('confirm_delete') # id passed in url
        try:
            year = Year.objects.get(pk=year_id)
            year_name = year.Year  # Store the name for the message
            year.delete()
            messages.success(request, f"L'Any {year_name} s'ha eliminat correctament.")
            return redirect('year_list') 
        except Year.DoesNotExist:
            messages.error(request, "Error: L'any no existeix.")
    
    # ACTION OF INITIAL DELETE
    if 'confirm_delete' in request.GET:
        year_id = request.GET.get('confirm_delete')
        deleting = year_id  # Only pass the ID

    return render(request, 'year_list_actions.html', {
        'years': years,
        'deleting': deleting,
    })

#Function to create or edit a year - depends if is passed a idYear 
def year_create_edit(request,idYear=None):
    if idYear:
        # If idYear is passed, we are editing an existing Year
        year = get_object_or_404(Year, pk=idYear)
        if request.method == 'POST':
            form = YearForm(request.POST, instance=year)
            if form.is_valid():
                form.save()
                messages.success(request, f"L'any {year.Year} s\'ha actualitzat correctament.")
                return redirect('year_list')
        else:
            form = YearForm(instance=year)
    else:
        # No idYear, we are creating a new year
        if request.method == 'POST':
            form = YearForm(request.POST)
            if form.is_valid():
                new_year = form.save()
                messages.success(request, f"L'any {new_year.Year} s\'ha afegit correctament.")
                return redirect('year_list')
        else:
            form = YearForm()
    return render(request, 'year_form.html', {'form': form})