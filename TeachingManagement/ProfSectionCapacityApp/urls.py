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
from .import views

app_name=''

urlpatterns = [
    
    #For the PROFESSOR
    path('capacity-professors/', views.capacityprofessor_list, name='capacityprofessor_list'),
    path('capacity-professors/select/', views.capacityprofessor_select, name='capacityprofessor_select'),
    path('capacity-professors/edit/<int:idProfessor>', views.capacityprofessor_create_edit, name='capacityprofessor_edit'),
    path('capacity-professors/year/<int:idYear>', views.capacityprofessor_list_for_year, name='capacityprofessor_list_year'),


    # For adding, editing, and deleting Capacity, Free, and CapacitySection entries
    #GLOBAL CAPACITY
    path('capacity-professors/capacity/create/<int:idProfessor>', views.create_capacity, name='create_capacity'),
    path('capacity-professors/capacity/edit/<int:idCapacity>', views.edit_capacity, name='edit_capacity'),
    path('delete_capacity/<int:idCapacity>/', views.delete_capacity, name='delete_capacity'),

    #FREE CAPACITY
    path('capacity-professors/free/create/<int:idProfessor>', views.create_free, name='create_free'),
    path('capacity-professors/free/edit/<int:idFree>/', views.edit_free, name='edit_free'),
    path('delete_free/<int:idFree>/', views.delete_free, name='delete_free'),

    # #CAPACITY FOR SECTION PROFESSOR
    path('capacity-professors/capacity-section/create/<int:idProfessor>', views.create_capacity_section, name='create_capacity_section'),
    path('capacity-professors/capacity-section/edit/<int:idCapacitySection>', views.edit_capacity_section, name='edit_capacity_section'),
    path('delete_capacity-section/<int:idCapacitySection>/', views.delete_capacity_section, name='delete_capacity_section'),


    #For the SECTIONS
    path('capacity-section/', views.capacitysection_list, name='capacitysectio_list'),
    path('capacity-section/create/', views.capacitysection_create_edit, name='capacitysection_create'),
    path('capacity-section/edit/<int:idSection>', views.capacitysection_create_edit, name='capacitysection_edit'),
]
