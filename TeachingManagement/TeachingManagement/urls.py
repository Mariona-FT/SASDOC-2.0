"""
URL configuration for TeachingManagement project.

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
"""
from django.contrib import admin
from django.urls import path,include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('baseapp/', permanent=True)),  # Redirect root URL to /baseapp/

    path('baseapp/',include('TeachingManagementApp.urls')),  # URL for every APP - TeachingManagementApp
   
    #functionalities for users in app + their functionalities
    path('users/',include('UsersApp.urls')),  # URL for every APP - UsersApp
   
    #for Directors + their functions
    path('director/',include('DirectorApp.urls')),  # URL for every APP - DirectorApp
    path('academicinfo/',include('AcademicInfoApp.urls')),  # URL for every APP - AcademicInfoApp
    path('professorsection/',include('ProfSectionCapacityApp.urls')),  # URL for every APP - ProfSectionCapacity

    #For section chiefs + their functions
    path('sectionchief/',include('SectionChiefApp.urls')),  # URL for every APP - SectionChiefApp
    path('infosection/',include('AssignmentYearApp.urls')),  # URL for every APP - AssignmentYearApp

    path('admin/', admin.site.urls),
]
