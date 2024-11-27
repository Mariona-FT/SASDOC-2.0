from django.shortcuts import render
from django.contrib.auth.decorators import login_required,user_passes_test

# Create your views here.
def is_director(user):
    return user.role == 'director'

@login_required
@user_passes_test(is_director)
def director_dashboard(request):
    return render(request, 'director_dashboard.html')
