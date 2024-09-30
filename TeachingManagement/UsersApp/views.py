from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

def is_director(user):
    return user.role == 'director'

@login_required
#@user_passes_test(is_director)
def director_dashboard(request):
    pass
    #return render(request, 'users/director_dashboard.html')

def is_sector_chief(user):
    return user.role == 'sector_chief'

@login_required
#@user_passes_test(is_sector_chief)
def sector_chief_dashboard(request):
    pass
    #return render(request, 'users/sector_chief_dashboard.html')

def is_professor(user):
    return user.role == 'professor'

@login_required
#@user_passes_test(is_professor)
def professor_dashboard(request):
    pass
    #return render(request, 'users/professor_dashboard.html')