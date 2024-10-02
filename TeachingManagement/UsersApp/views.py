import pandas as pd
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .forms import CustomLoginForm, ProfessorRegistrationForm,ChiefRegistrationForm, UploadFileForm # customized forms in forms.py
from .models import Professor,Chief, CustomUser

# Create your views here.

def is_director(user):
    return user.role == 'director'

@login_required
@user_passes_test(is_director)
def director_dashboard(request):
    return render(request, 'users/director_dashboard.html')

def is_sector_chief(user):
    return user.role == 'sector_chief'

@login_required
@user_passes_test(is_sector_chief)
def sector_chief_dashboard(request):
    return render(request, 'users/sectorchief_dashboard.html')

def is_professor(user):
    return user.role == 'professor'

@login_required
@user_passes_test(is_professor)
def professor_dashboard(request):
    return render(request, 'users/professor_dashboard.html')

#REGISTER PROFESSOR - only for DIRECTOR
@login_required
@user_passes_test(is_director)
def register_professor(request):
   
    if request.method == 'POST':
        form = ProfessorRegistrationForm(request.POST)
       
        if form.is_valid():
            user=form.save()  # The form's save method already handles user and professor creation
            print(f"User saved: {user.username}")

            return redirect('Home')  # Redirect to a success page
    else:           
        form = ProfessorRegistrationForm()

    return render(request, 'actions/register_professor.html', {'form': form})

#REGISTER PROFESSOR - only for DIRECTOR - USING CSV or EXCEL
@login_required
@user_passes_test(is_director)
def upload_professors(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                # Check file format and read content
                if file.name.endswith('.csv'):
                    data = pd.read_csv(file)
                elif file.name.endswith('.xlsx'):
                    data = pd.read_excel(file)
                else:
                    messages.error(request, "Tipus de fitxer no suportat.")
                    return redirect('upload_professors')

                # Validate columns in the file
                required_columns = ['nom', 'cognom', 'email', 'descripcio', 'comentaris', 'esactiu']
                if not all(column in data.columns for column in required_columns):
                    messages.error(request, f"El fitxer ha de contenir exactament les següents columnes: {', '.join(required_columns)}")
                    return redirect('upload_professors')

                # Loop through the data and update/create professors
                for index, row in data.iterrows():
                    try:
                        username = f"{row['nom']}.{row['cognom']}".lower()
                        password = f"{row['nom'].lower()}_{row['cognom'].lower()}"  # Create password

                        # Check if the user already exists
                        user, created = CustomUser.objects.get_or_create(
                            username=username,
                            defaults={
                                'first_name': row['nom'],
                                'last_name': row['cognom'],
                                'email': row['email'],
                                'role': 'professor'
                            }
                        )

                        if created:
                            user.password = make_password(password)  # Hash the password
                            user.save()
                            messages.success(request, f"Professor {user.first_name} {user.last_name} creat correctament.")
                        else:
                            # Update user information if already exists
                            user.first_name = row['nom']
                            user.last_name = row['cognom']
                            user.email = row['email']
                            user.save()
                            messages.info(request, f"Professor {user.first_name} {user.last_name} actualitzat correctament.")

                        # Update or create Professor instance
                        Professor.objects.update_or_create(
                            user=user,
                            defaults={
                                'name': row['nom'],
                                'family_name': row['cognom'],
                                'email': row['email'],
                                'description': row['descripcio'],
                                'comment': row['comentaris'],
                                'isActive': row['esactiu']
                            }
                        )

                    except Exception as e:
                        # Handle errors specific to each row with a friendly message
                        messages.warning(request, f"Error actualitzant el professor {row['nom']} {row['cognom']}.")
                
                messages.success(request, f"Professors pujats correctament.")
                return redirect('upload_professors')

            except Exception as e:
                messages.error(request, f"Error de processament del fitxer: {str(e)}")
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
        if form.is_valid():
            chief = form.save(commit=False)
            chief.professor = form.cleaned_data['professor']
            chief.save()
            return redirect('Home')  # Redirect to a success page
    else:
        form = ChiefRegistrationForm()
    return render(request, 'actions/register_chief.html', {'form': form,'professors':professors})

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