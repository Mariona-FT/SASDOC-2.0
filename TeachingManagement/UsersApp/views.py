from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def director_dashboard(request):
    pass
    #return render(request, 'users/director_dashboard.html')

@login_required
def sector_chief_dashboard(request):
    pass
    #return render(request, 'users/sector_chief_dashboard.html')

@login_required
def professor_dashboard(request):
    pass
    #return render(request, 'users/professor_dashboard.html')