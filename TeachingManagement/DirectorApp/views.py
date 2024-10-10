from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def director_dashboard(request):
    return render(request, 'director_dashboard.html')

@login_required
def test_director_navbar(request):
    return render(request, 'navbars/test-navbar-director.html')