from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import login, authenticate, logout
from .forms import CustomLoginForm, ProfessorRegistrationForm,ChiefRegistrationForm # customized forms in forms.py
from .models import Professor,Chief

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
            form.save()  # The form's save method already handles user and professor creation
            return redirect('Home')  # Redirect to a success page
    else:
        form = ProfessorRegistrationForm()

    return render(request, 'actions/register_professor.html', {'form': form})

#REGISTER CHEIF
@login_required
@user_passes_test(is_director)
def register_chief(request):
    if request.method == 'POST':
        form = ChiefRegistrationForm(request.POST)
        if form.is_valid():
            chief = form.save(commit=False)
            chief.professor = form.cleaned_data['professor']  # Associate with the selected professor
            chief.save()
            return redirect('Home')  # Redirect to a success page
    else:
        form = ChiefRegistrationForm()
    return render(request, 'actions/register_chief.html', {'form': form})

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