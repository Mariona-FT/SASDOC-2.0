import pandas as pd
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .forms import CustomLoginForm, ProfessorRegistrationForm,ExtraInfoProfessor,ChiefRegistrationForm, UploadFileForm # customized forms in forms.py
from .models import Professor,Chief, CustomUser
from .services import  process_professor_file #services of the app
from django.db import IntegrityError


# Create your views here.

#DIRECTOR views
def is_director(user):
    return user.role == 'director'

@login_required
@user_passes_test(is_director)
def redirect_director_dashboard(request):
    return render(request, 'directorapp/director_dashboard.html')

#SECTOR CHIEF views
def is_sector_chief(user):
    return user.role == 'sector_chief'

@login_required
@user_passes_test(is_sector_chief)
def sector_chief_dashboard(request):
    #Delete this dashboard in the future
    return render(request, 'users/sectorchief_dashboard.html')

#PROFESSOR views
def is_professor(user):
    return user.role == 'professor'

@login_required
@user_passes_test(is_professor)
def professor_dashboard(request):
    #Delete this dashboard in the future
    return render(request, 'users/professor/professor_dashboard.html')


### PROFESSOR ###
@login_required
@user_passes_test(is_director)
def professor_crud(request):
    professors = Professor.objects.all()
    deleting = None

    if request.method == "POST":
        # Handle delete confirmation
        if 'confirm_delete' in request.POST:
            professor_id = request.POST.get('confirm_delete')
            professor = get_object_or_404(Professor, pk=professor_id)
            professor_name = f"{professor.name} {professor.family_name}"
            professor.delete()
            messages.success(request, f"El professor {professor_name} s'ha eliminat correctament.")
            return redirect('usersapp:professor_crud')

    # Handle initial delete confirmation
    if 'confirm_delete' in request.GET:
        professor_id = request.GET.get('confirm_delete')
        deleting = get_object_or_404(Professor, pk=professor_id)

    return render(request, 'users/professor/professor_crud.html', {
        'professors': professors,
        'deleting': deleting,
    })

@login_required
@user_passes_test(is_director)
def create_professor_view(request):
    if request.method == 'POST':
        form = ProfessorRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Save the user (CustomUser) but do not commit yet
                user = form.save(commit=True)
                user.role = 'professor' 
                user.save()

                messages.success(request, f"Professor {user.first_name} {user.last_name} s'ha creat correctament.")
                return redirect('usersapp:professor_crud')
            
            except IntegrityError as e:
                # Add an error message to the form for the user to correct it
                form.add_error(None, f"Error: No es pot crear el professor. {str(e)}")
        else:
            messages.error(request, "Formulari no vàlid. Revisa les dades i torna-ho a intentar.")

    else:
        form = ProfessorRegistrationForm()

    return render(request, 'users/professor/professor_form.html', {'form': form})

@login_required
@user_passes_test(is_director)
def edit_professor_view(request, professor_id):
       # Retrieve the professor by ID, or return a 404 error
    professor = get_object_or_404(Professor, pk=professor_id)
    user = professor.user  # Get the linked CustomUser instance

    if request.method == 'POST':
        form = ProfessorRegistrationForm(request.POST, instance=user)  # Use the related user instance
        if form.is_valid():
            # Save the CustomUser (user) details
            if user.role != 'sector_chief':  
                user.role = 'professor' 
            form.save()
            
            messages.success(request, f"El professor {professor.name} {professor.family_name} s'ha actualitzat correctament.")
            return redirect('usersapp:professor_crud')
    else:
        # Populate the form with the current user's and professor's information
        try:
            form = ProfessorRegistrationForm(initial={
                'idprofessor': professor.idProfessor,
                'username': professor.user.username,
                'name': professor.name,
                'family_name': professor.family_name,
                'description': professor.description,
                'comment': professor.comment,
                'email': professor.email,
                'isactive': professor.isActive,
            }, instance=professor.user)
        except Professor.DoesNotExist:
            messages.error(request, "No hi ha professor amb el ID de usuari donat.")
            return redirect('usersapp:professor_crud')

    return render(request, 'users/professor/professor_form.html', {'form': form})

def extrainfo_professor_crud(request):
    professors = Professor.objects.all()
    deleting = None

    incomplete_count = 0
    for professor in professors:
        if not professor.current_contract or not professor.professor_fields.exists() or not professor.professor_languages.exists():
            incomplete_count += 1

    if request.method == "POST":
        # Handle delete confirmation
        if 'confirm_delete' in request.POST:
            professor_id = request.POST.get('confirm_delete')
            professor = get_object_or_404(Professor, pk=professor_id)
            professor_name = f"{professor.name} {professor.family_name}"
            professor.delete()
            messages.success(request, f"El professor {professor_name} s'ha eliminat correctament.")
            return redirect('usersapp:extrainfo_professor_crud')

    # Handle initial delete confirmation
    if 'confirm_delete' in request.GET:
        professor_id = request.GET.get('confirm_delete')
        deleting = get_object_or_404(Professor, pk=professor_id)

    return render(request, 'users/professor/professor_extrainfo_crud.html', {
        'professors': professors,
        'deleting': deleting,
        'incomplete_count': incomplete_count,
    })



@login_required
@user_passes_test(is_director)
def enter_extrainfo_professor(request,professor_id):
    professor = get_object_or_404(Professor, pk=professor_id)

    if request.method == 'POST':
        form = ExtraInfoProfessor(request.POST, instance=professor)
        if form.is_valid():
            form.save()
            messages.success(request, f"Informació extra per a {professor.name} {professor.family_name} actualitzada correctament.")
            return redirect('usersapp:extrainfo_professor_crud')
        else:
            messages.warning(request, f"Informació extra per a {professor.name} {professor.family_name} no s'ha actualitzat correctament.")

    else:
        form = ExtraInfoProfessor(instance=professor) #enter information of the professor - 

    return render(request, 'users/professor/professor_extrainfo_form.html', {'form': form,'professor':professor})

#Professor list to manage - listing and actions of edit, delete and add professors
def professor_list(request):
    professors = Professor.objects.all().order_by('family_name')
    deleting = None

    if request.method == "POST" and 'confirm_delete' in request.POST:
        # FINAL DELETE
        professor_id = request.POST.get('confirm_delete')
        try:
            professor = Professor.objects.get(pk=professor_id)
            professor_name = f"{professor.name} {professor.family_name}"
            professor.delete()
            messages.success(request, f"El professor {professor_name} s'ha eliminat correctament.")
            return redirect('usersapp:professor_list')
        except Professor.DoesNotExist:
            messages.error(request,"Error: El professor no existeix i no s'ha pogut borrar.")

    # Handle initial delete confirmation
    if 'confirm_delete' in request.GET:
        professor_id = request.GET.get('confirm_delete')
        deleting = professor_id

    return render(request, 'users/professor/professor_list_actions.html', {
        'professors': professors,
        'deleting': deleting,
    })

#Function to create or edit a Professor - depends if is passed a idProfessor 
def professor_create_edit(request, idProfessor=None):
    pass


# REGISTER PROFESSOR - only for DIRECTOR - USING CSV or EXCEL
@login_required
@user_passes_test(is_director)
def upload_professors(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if process_professor_file(file, request):
                return redirect('usersapp:upload_professors')
    else:
        form = UploadFileForm()

    return render(request, 'actions/upload_professors.html', {'form': form})

#SECTOR CHIEF 
#Sector chief list to manage - listing and actions of edit, delete and add sector chiefs
def sectorchief_list(request):
    professors = Professor.objects.all()
    deleting = None
   
    if request.method == "POST" and 'confirm_delete' in request.POST:
       # FINAL DELETE
        chief_id = request.POST.get('confirm_delete')  # ID passed in url
        try:
            # Fetch the Chief instance by id
            chief = Chief.objects.get(pk=chief_id)
            professor = chief.professor 
            professor_name = f"{professor.name} {professor.family_name}"  
            chief.delete()

            # Check if the professor still has any Chief records
            if not professor.chief_set.exists():
                professor.user.role = 'professor'
                professor.user.save()

            messages.success(request, f"El Cap de secció {professor_name} s'ha eliminat correctament.")
            return redirect('usersapp:sectorchief_list')

        except Chief.DoesNotExist:
            messages.error(request, "Error: El Cap de Secció no existeix.")
        except Exception as e:  # Catch any other exceptions
            messages.error(request, f"Error inesperat: {str(e)}")
    
    # ACTION OF INITIAL DELETE
    if 'confirm_delete' in request.GET:
        chief_id = request.GET.get('confirm_delete')
        deleting = chief_id  # Only pass the ID

    return render(request, 'users/sectorchief/sectorchief_list_actions.html', {
        'professors': professors,
        'deleting': deleting,
    })

#Function to create or edit a Section Chief - depends if is passed a idChief 
def sectorchief_create_edit(request, idChief=None):
    if idChief:
        # If idChief is passed, we are editing an existing chief
        chief = get_object_or_404(Chief, pk=idChief)

        if request.method == 'POST':
            form = ChiefRegistrationForm(request.POST, instance=chief)
            if form.is_valid():
                new_chief = form.save()  
                messages.success(request, f"El Cap de secció {chief.professor.name} {chief.professor.family_name} s'ha actualitzat correctament.")
                return redirect('usersapp:sectorchief_list')
        else:
            form = ChiefRegistrationForm(instance=chief)
    else:
        # NO idChief, create a new chief
        form = ChiefRegistrationForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            new_chief = form.save()
            messages.success(request, f"El Cap de secció {new_chief.professor.name} {new_chief.professor.family_name} s'ha afegit correctament.")
            return redirect('usersapp:sectorchief_list')
        
    return render(request, 'users/sectorchief/sectorchief_form.html', {'form': form})

#LOGIN
def login_session(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        
        if form.is_valid():
             if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(request, username=username, password=password)
                
                if user is not None:
                    login(request, user)
                
                # Check user role and redirect accordingly
                    if user.role == 'director':
                        return redirect('directorapp:director_dashboard')  # URL for Director
                    elif user.role == 'sector_chief':
                        return redirect('usersapp:sector_chief_dashboard')  # URL for Sector Chief
                    elif user.role ==  'professor':
                        return redirect('usersapp:professor_dashboard')  # URL for Professor
                else:
                    return render(request, 'actions/login.html', {'error': 'Invalid credentials'})
    else:
        form = CustomLoginForm()


    return render(request, 'actions/login.html', {'form': form})

#LOGOUT
def logout_session(request):
    logout(request)
    return redirect('Home')