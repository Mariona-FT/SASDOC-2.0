import pandas as pd
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .forms import CustomLoginForm, ProfessorRegistrationForm,ChiefRegistrationForm, UploadFileForm # customized forms in forms.py
from .models import Professor,Chief, CustomUser
from .services import register_professor_form, process_professor_file #services of the app


# Create your views here.

#DIRECTOR views
def is_director(user):
    return user.role == 'director'

@login_required
@user_passes_test(is_director)
def director_dashboard(request):
    return render(request, 'users/director_dashboard.html')

#SECTOR CHIEF views
def is_sector_chief(user):
    return user.role == 'sector_chief'

@login_required
@user_passes_test(is_sector_chief)
def sector_chief_dashboard(request):
    return render(request, 'users/sectorchief_dashboard.html')

#PROFESSOR views
def is_professor(user):
    return user.role == 'professor'

@login_required
@user_passes_test(is_professor)
def professor_dashboard(request):
    return render(request, 'users/professor_dashboard.html')


# REGISTER PROFESSOR MANUALLY - only for DIRECTOR
@login_required
@user_passes_test(is_director)
def register_professor(request):
    if request.method == 'POST':
        form = ProfessorRegistrationForm(request.POST)
        if form.is_valid():
            user = register_professor_form(form,request)
            return redirect('register_professor')  
    else:
        form = ProfessorRegistrationForm()

    return render(request, 'actions/register_professor.html', {'form': form})


# REGISTER PROFESSOR - only for DIRECTOR - USING CSV or EXCEL
@login_required
@user_passes_test(is_director)
def upload_professors(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if process_professor_file(file, request):
                return redirect('upload_professors')
    else:
        form = UploadFileForm()

    return render(request, 'actions/upload_professors.html', {'form': form})

#REGISTER CHEIF
@login_required
@user_passes_test(is_director)
def register_chief(request):
    
    professors = Professor.objects.all()  # Fetch all professors

    if request.method == 'POST':
        form = ChiefRegistrationForm(request.POST)
        professor_id = request.POST.get('professor')  # Get the professor ID from the submitted data

        if form.is_valid() and professor_id:
            chief = form.save(commit=False)
            # Fetch the professor based on the ID
            try:
                professor = Professor.objects.get(idProfessor=professor_id)
                
                # Check if this professor is already a sector chief
                if professor.user.role == 'sector_chief':
                    messages.warning(request, "Aquest professor ja és cap de secció.")
                    return render(request, 'actions/register_chief.html', {'form': form, 'professors': professors})

            except Professor.DoesNotExist:
                form.add_error(None, 'Selected professor does not exist.')
                return render(request, 'actions/register_chief.html', {'form': form, 'professors': professors})
            
            
            chief.save()
            
            # Update the professor's user role
            professor = chief.professor 
            professor.user.role = 'sector_chief'
            professor.user.save()  
            
            messages.success(request, f"Professor {professor.name} {professor.family_name} triat per ser cap de secció: {chief.section}.")
            return redirect('register_chief')
        
        # If the form is not valid or professor_id is missing, display the errors
        if not professor_id:
            form.add_error('professor', 'Tria un professor per ser cap de secció.')  # Add error to the form

            messages.warning(request,f"Tria un professor per ser cap de secció.")
            return redirect('register_chief')
            
    else:
        form = ChiefRegistrationForm()
        
    return render(request, 'actions/register_chief.html', {'form': form, 'professors': professors})

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
                        return redirect('director_dashboard')  # URL for Director
                    elif user.role == 'sector_chief':
                        return redirect('sector_chief_dashboard')  # URL for Sector Chief
                    elif user.role ==  'professor':
                        return redirect('professor_dashboard')  # URL for Professor
                else:
                    return render(request, 'actions/login.html', {'error': 'Invalid credentials'})
    else:
        form = CustomLoginForm()


    return render(request, 'actions/login.html', {'form': form})

#LOGOUT
def logout_session(request):
    logout(request)
    return redirect('Home')