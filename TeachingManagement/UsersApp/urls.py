"""
URL configuration for WebProject project - APP

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

  **  URL ONLY FOR THIS APP **
"""
from django.urls import path
from . import views

app_name = 'usersapp'

urlpatterns = [
    # use names for easy calls + functions reverse() and {% url %}  
    path('login/', views.login_session, name='login'),
    path('logout/', views.logout_session, name='logout'),

    #Professors
    path('professor-management/', views.professor_crud, name='professor_crud'),
    path('professor-information/', views.extrainformation_professor, name='info_professor'),

    path('professor-create/', views.create_professor_view, name='create_professor'),
    path('professor-edit/<int:professor_id>/', views.edit_professor_view, name='edit_professor'),
    path('professor-upload/', views.upload_professors, name='upload_professors'),

    #Sector chiefs
    path('sectorchief-management/', views.sectorchief_crud, name='sectorchief_crud'),
    path('register-chief/', views.register_chief, name='register_chief'),
 
    #Dashboards
    path('director/', views.redirect_director_dashboard, name='redirect_director_dashboard'),
    path('sector-chief/', views.sector_chief_dashboard, name='sector_chief_dashboard'),
    path('professor/', views.professor_dashboard, name='professor_dashboard'),
    ]