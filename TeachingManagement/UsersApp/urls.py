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
    path('professor/', views.professor_list, name='professor_list'),
    path('professor/create/', views.professor_create_edit, name='professor_create'),
    path('professor/edit/<int:idProfessor>', views.professor_create_edit, name='professor_edit'),
    path('professor/upload/', views.upload_professors, name='upload_professors'), #for file

    #Section chiefs
    path('sectionchief/', views.sectionchief_list, name='sectionchief_list'),
    path('sectionchief/create/', views.sectionchief_create_edit, name='sectionchief_create'),
    path('sectionchief/edit/<int:idChief>', views.sectionchief_create_edit, name='sectionchief_edit'),
 
    #provisional Dashboards
    path('dashprofessor/', views.professor_dashboard, name='professor_dashboard'),
    ]