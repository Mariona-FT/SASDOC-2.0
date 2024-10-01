from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

def home_page(request):
    if request.user.is_authenticated:
    # Redirect authenticated users to their dashboard based on role
        if request.user.role == 'director':
            return redirect('director_dashboard')
        elif request.user.role == 'sector_chief':
            return redirect('sector_chief_dashboard')
        elif request.user.role == 'professor':
            return redirect('professor_dashboard')
    else:
        # For unauthenticated users, show the home page
        return render(request, 'home.html')