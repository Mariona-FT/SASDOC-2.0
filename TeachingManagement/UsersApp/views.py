import pandas as pd
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .forms import CustomLoginForm,ProfessorForm,ChiefRegistrationForm, UploadFileForm # customized forms in forms.py
from .models import Professor,Chief, CustomUser
from .services import  process_professor_file #services of the app
from django.db import IntegrityError


# Create your views here.

#DIRECTOR views
def is_director(user):
    return user.role == 'director'

#SECTION CHIEF views
def is_section_chief(user):
    return user.role == 'section_chief'

#PROFESSOR views
def is_professor(user):
    return user.role == 'professor'

@login_required
@user_passes_test(is_professor)
def professor_dashboard(request):
    #Delete this dashboard in the future
    return render(request, 'users/professor/professor_dashboard.html')


### PROFESSOR ###
#Professor list to manage - listing and actions of edit, delete and add professors
@login_required
@user_passes_test(is_director)
def professor_list(request):
    professors = Professor.objects.all().order_by('family_name')
    deleting = None

    if request.method == "POST" and 'confirm_delete' in request.POST:
        # FINAL DELETE
        
        professor_id = request.POST.get('confirm_delete')

        try:
            professor = Professor.objects.get(idProfessor=professor_id)
            professor_name = f"{professor.name} {professor.family_name}"

            user = professor.user
            if user:
                user.delete()  # Delete the user

            professor.delete()
            messages.success(request, f"El professorat amb el nom {professor_name} s'ha eliminat correctament.")
            return redirect('usersapp:professor_list')
        except Professor.DoesNotExist:
            messages.error(request,"Error: El professorat no existeix i no s'ha pogut borrar.")

    # Handle initial delete confirmation
    if 'confirm_delete' in request.GET:
        professor_id = request.GET.get('confirm_delete')
        deleting = professor_id

    return render(request, 'users/professor/professor_list_actions.html', {
        'professors': professors,
        'deleting': deleting,
    })

#Function to create or edit a Professor - depends if is passed a idProfessor 
@login_required
@user_passes_test(is_director)
def professor_create_edit(request, idProfessor=None):

    if idProfessor:
        # If idProfessor is passed, we are editing an existing courses
        professor = get_object_or_404(Professor, idProfessor=idProfessor)
        user = professor.user  # Get the related CustomUser instance

        if request.method == 'POST':
            form = ProfessorForm(request.POST, instance=user, professor=professor)
           
            if form.is_valid():
                form.save(commit=True)  # Save without changing role
                messages.success(request, f"El professorat {professor.name} {professor.family_name} s\'ha actualitzat correctament.")
                return redirect('usersapp:professor_list')
            else:
                messages.error(request, f"El professorat no s\'ha actualitzat correctament.")

        else:
            form = ProfessorForm(instance=user, professor=professor)
    else:
        # No idProfessor, we are creating a new course
        if request.method == 'POST':
            form = ProfessorForm(request.POST)
            if form.is_valid():
                user = form.save(commit=True)  # Save the user but don't commit yet
                user.role = 'professor'  # Set the role to 'professor'
                user.save()  # Now save the user to the database
                new_professor = form.save()
                messages.success(request, f"El professorat {new_professor.first_name} {new_professor.last_name} s\'ha afegit correctament.")
                return redirect('usersapp:professor_list')
            else:
                messages.error(request, f"El professorat no s\'ha creat correctament.")
        else:
            form = ProfessorForm()
    return render(request, 'users/professor/professor_form.html', {'form': form})



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

#SECTION CHIEF 
#section chief list to manage - listing and actions of edit, delete and add section chiefs
def sectionchief_list(request):
    professors = Professor.objects.all().order_by('family_name')
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

            messages.success(request, f"El cap de secció {professor_name} s'ha eliminat correctament.")
            return redirect('usersapp:sectionchief_list')

        except Chief.DoesNotExist:
            messages.error(request, "Error: El cap de secció no existeix.")
        except Exception as e:  # Catch any other exceptions
            messages.error(request, f"Error inesperat: {str(e)}")
    
    # ACTION OF INITIAL DELETE
    if 'confirm_delete' in request.GET:
        chief_id = request.GET.get('confirm_delete')
        deleting = chief_id  # Only pass the ID

    return render(request, 'users/sectionchief/sectionchief_list_actions.html', {
        'professors': professors,
        'deleting': deleting,
    })

#Function to create or edit a Section Chief - depends if is passed a idChief 
def sectionchief_create_edit(request, idChief=None):
    if idChief:
        # If idChief is passed, we are editing an existing chief
        chief = get_object_or_404(Chief, pk=idChief)

        if request.method == 'POST':
            form = ChiefRegistrationForm(request.POST, instance=chief)
            if form.is_valid():
                new_chief = form.save()  
                messages.success(request, f"El cap de secció {chief.professor.name} {chief.professor.family_name} s'ha actualitzat correctament.")
                return redirect('usersapp:sectionchief_list')
        else:
            form = ChiefRegistrationForm(instance=chief)
    else:
        # NO idChief, create a new chief
        form = ChiefRegistrationForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            new_chief = form.save()
            messages.success(request, f"El cap de secció {new_chief.professor.name} {new_chief.professor.family_name} s'ha afegit correctament.")
            return redirect('usersapp:sectionchief_list')
        
    return render(request, 'users/sectionchief/sectionchief_form.html', {'form': form})

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
                    elif user.role == 'section_chief':
                        return redirect('sectionchiefapp:sectionchief_dashboard')  # URL for Section Chief
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