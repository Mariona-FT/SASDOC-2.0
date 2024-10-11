import pandas as pd
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .forms import CustomLoginForm, ProfessorRegistrationForm,ChiefRegistrationForm, UploadFileForm # customized forms in forms.py
from .models import Professor,Chief, CustomUser
from .services import  process_professor_file #services of the app


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
    return render(request, 'users/sectorchief_dashboard.html')

#PROFESSOR views
def is_professor(user):
    return user.role == 'professor'

@login_required
@user_passes_test(is_professor)
def professor_dashboard(request):
    return render(request, 'users/professor_dashboard.html')


### PROFESSOR ###
def professor_crud(request):
    professors = Professor.objects.all()
    form = ProfessorRegistrationForm()  # Use the registration form
    deleting = None

    if request.method == "POST":
        # Handle delete confirmation
        if 'confirm_delete' in request.POST:
            professor_id = request.POST.get('confirm_delete')
            print(f"Request to delete professor with ID {professor_id}")
            professor = get_object_or_404(Professor, pk=professor_id)
            professor_name = f"{professor.name} {professor.family_name}"
            professor.delete()
            messages.success(request, f"El professor {professor_name} s'ha eliminat correctament.")
            return redirect('usersapp:professor_crud')

        # Handle update
        if 'idProfessor' in request.POST:
            professor_id = request.POST.get('idProfessor')
            print(f"Request to update professor with ID {professor_id}")

            professor = get_object_or_404(Professor, pk=professor_id)
            form = ProfessorRegistrationForm(request.POST, instance=professor.user)  # Update user instance
            if form.is_valid():
                print("Form is valid for update")

                form.save()  # Save the user
                # Update associated Professor instance
                professor.idProfessor = form.cleaned_data['idprofessor']
                professor.name = form.cleaned_data['name']
                professor.family_name = form.cleaned_data['family_name']
                professor.description = form.cleaned_data['description']
                professor.comment = form.cleaned_data['comment']
                professor.email = form.cleaned_data['email']
                professor.isActive = form.cleaned_data['isactive']
                professor.save()  # Save the Professor instance
                print(f"Professor {professor.name} {professor.family_name} updated successfully")

                messages.success(request, f"El professor {professor.name} {professor.family_name} s'ha actualitzat correctament.")
                return redirect('usersapp:professor_crud')

        # Handle create
        else:
            form = ProfessorRegistrationForm(request.POST)
            if form.is_valid():
                try:
                    # Save the form, which handles user creation/updating
                    user = form.save()
                    messages.success(request, f"Professor {user.first_name} {user.last_name} creat correctament.")
                    return redirect('usersapp:professor_crud')

                except Exception as e:
                    print(f"Error in registering professor: {str(e)}")  # Debugging line
                    messages.error(request, "Error al registrar el professor.")
            else:
                print(form.errors)  # Debugging line
                messages.error(request, "Errors in the form. Please fix them and try again.")  


    # Handle edit
    if 'edit' in request.GET:
        professor_id = request.GET.get('edit')
        professor = get_object_or_404(Professor, pk=professor_id)
        print(f"Request to edit professor with ID {professor_id}")

        # Pre-fill the form with the current user's data
        form = ProfessorRegistrationForm(initial={
            'idprofessor': professor.idProfessor,
            'name': professor.name,
            'family_name': professor.family_name,
            'description': professor.description,
            'comment': professor.comment,
            'email': professor.email,
            'isactive': professor.isActive,
        })

    # Handle initial delete confirmation
    if 'confirm_delete' in request.GET:
        professor_id = request.GET.get('confirm_delete')
        print(f"Request to confirm delete for professor with ID {professor_id}")

        deleting = get_object_or_404(Professor, pk=professor_id)

    return render(request, 'users/professor_crud.html', {
        'form': form,
        'professors': professors,
        'deleting': deleting,
        'idProfessor': professor.pk if 'edit' in request.GET else None,

    })

# REGISTER PROFESSOR MANUALLY - only for DIRECTOR
@login_required
@user_passes_test(is_director)
def register_professor(request):
    if request.method == 'POST':
            form = ProfessorRegistrationForm(request.POST)
            if form.is_valid():
                try:
                    # Save the form, which handles user creation/updating
                    user = form.save()

                    messages.success(request, f"Professor {user.first_name} {user.last_name} creat correctament.")
                    return redirect('usersapp:register_professor')

                except Exception as e:
                    print(f"Error in registering professor: {str(e)}")  # Debugging line
                    messages.error(request, "Error al registrar el professor.")
            else:
                print(form.errors)  # Debugging line
                messages.error(request, "Errors in the form. Please fix them and try again.")   
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
                        return redirect('directorapp:director_dashboard')  # URL for Director
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