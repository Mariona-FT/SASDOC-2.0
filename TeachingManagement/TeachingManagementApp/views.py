from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

def home_page(request):
    if request.user.is_authenticated:
    # Redirect authenticated users to their dashboard based on role
        if request.user.role == 'director':
            return redirect('directorapp:director_dashboard')
        elif request.user.role == 'section_chief':
            return redirect('sectionchiefapp:sectionchief_dashboard')
        elif request.user.role == 'professor':
            return redirect('professorapp:professor_dashboard')
    
        # For unauthenticated users, show the home page
    return render(request, 'home.html')

def access_denied(request):
    return render(request, 'access_denied.html')
