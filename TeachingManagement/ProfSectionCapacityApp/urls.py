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
from .import views,services

app_name=''

urlpatterns = [
    
    #For the PROFESSOR
    path('capacity-professors/', views.capacityprofessor_list, name='capacityprofessor_list'),
    path('capacity-professors/select/', views.capacityprofessor_select, name='capacityprofessor_select'),
    path('capacity-professors/show/<int:idProfessor>', views.capacityprofessor_show, name='capacityprofessor_show'),

    path('capacity-professors/export/<int:year_id>', services.generate_capacityprofessor_excel, name='capacityprofessor_export'),
    path('capacity-professors/upload/', services.upload_capacityprofessor_excel, name='capacityprofessor_upload'),

    # For adding, editing, and deleting Capacity, Free, and CapacitySection entries
    
        #PROFESSOR GLOBAL CAPACITY
    path('capacity-professors/capacity/create/<int:idProfessor>', views.create_capacity, name='create_capacity'),
    path('capacity-professors/capacity/edit/<int:idCapacity>', views.edit_capacity, name='edit_capacity'),
    path('delete_capacity/<int:idCapacity>/', views.delete_capacity, name='delete_capacity'),

        #PROFESSOR FREE CAPACITY
    path('capacity-professors/free/create/<int:idProfessor>', views.create_free, name='create_free'),
    path('capacity-professors/free/edit/<int:idFree>/', views.edit_free, name='edit_free'),
    path('delete_free/<int:idFree>/', views.delete_free, name='delete_free'),

        #PROFESSOR CAPACITY FOR EVERY SECTION 
    path('capacity-professors/capacity-section/create/<int:idProfessor>', views.create_capacity_section, name='create_capacity_section'),
    path('capacity-professors/capacity-section/edit/<int:idCapacitySection>', views.edit_capacity_section, name='edit_capacity_section'),
    path('delete_capacity-section/<int:idCapacitySection>/', views.delete_capacity_section, name='delete_capacity_section'),


    #For the SECTIONS
    path('section-typepoints/', views.section_typepoints_list, name='sectiontypepoints_list'),    
    path('section-typepoints/create/', views.create_typepoints, name='create_typepoints'),
    path('section-typepoints/edit/<int:idTypePoints>/', views.edit_typepoints, name='edit_typepoints'),
    path('section-typepoints/delete/<int:idTypePoints>/', views.delete_typepoints, name='delete_typepoints'),

    #For the COURSES
    path('course-year/', views.course_year_list, name='courseyear_list'),
    path('course-year/create/', views.create_courseyear, name='create_courseyear'),
    path('course-year/edit/<int:idCourseYear>/', views.edit_courseyear, name='edit_courseyear'),
    path('courses-year/delete/<int:idCourseYear>/', views.delete_courseyear, name='delete_courseyear'),

    path('course-year/export/<int:year_id>', services.generate_courseyear_excel, name='courseyear_export'),
    path('course-year/upload/', services.upload_courseyear_excel, name='courseyear_upload'),

]
