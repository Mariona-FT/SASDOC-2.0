from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import CustomLoginForm # customized login - forms.py

# Create your views here.

def is_director(user):
    return user.role == 'director'

@login_required
#@user_passes_test(is_director)
def director_dashboard(request):
    return render(request, 'users/director_dashboard.html')

def is_sector_chief(user):
    return user.role == 'sector_chief'

@login_required
#@user_passes_test(is_sector_chief)
def sector_chief_dashboard(request):
    return render(request, 'users/sectorchief_dashboard.html')

def is_professor(user):
    return user.role == 'professor'

@login_required
#@user_passes_test(is_professor)
def professor_dashboard(request):
    return render(request, 'users/professor_dashboard.html')

def login_session(request):

    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Check user role and redirect accordingly
            if user.role == 'director':
                return redirect('director_dashboard')  # URL for Director
            elif user.role == 'sector_chief':
                return redirect('sector_chief_dashboard')  # URL for Sector Chief
            elif user.role == 'professor':
                return redirect('professor_dashboard')  # URL for Professor

    else:
        form = CustomLoginForm()

    return render(request, 'actions/login.html', {'form': form})


def logout_session(request):
    logout(request)
    return redirect('Home')