from django.shortcuts import render
from django.contrib.auth.decorators import login_required,user_passes_test

# Create your views here

def is_professor(user):
    return user.role == 'professor'

@login_required
@user_passes_test(is_professor)
def professor_dashboard(request):
    return render(request, 'professor_dashboard.html')

@login_required
@user_passes_test(is_professor)
def info_assignments(request):
    return render(request, 'info_assignments_professor.html')
