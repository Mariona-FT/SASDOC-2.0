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

urlpatterns = [

    #FIELD ACTIONS
    path('fields/', views.field_list, name='field_list'),
    path('fields/create/', views.field_create_edit, name='field_create'),
    path('fields/edit/<int:idField>', views.field_create_edit, name='field_edit'),

    #SECTIONS ACTIONS
    path('sections/', views.section_list, name='section_list'),
    path('sections/create/', views.sections_create_edit, name='section_create'),
    path('sections/edit/<int:idSection>', views.sections_create_edit, name='section_edit'),

    #SCHOOLS ACTIONS
    path('schools/', views.school_list, name='school_list'),
    path('schools/create/', views.school_create_edit, name='school_create'),
    path('schools/edit/<int:idSchool>', views.school_create_edit, name='school_edit'),

    #DEGREE ACTIONS
    path('degrees/', views.degree_list, name='degree_list'),
    path('degrees/create/', views.degree_create_edit, name='degree_create'),
    path('degrees/edit/<int:idDegree>', views.degree_create_edit, name='degree_edit'),

    #COURSES ACTIONS
    path('courses/', views.course_list, name='course_list'),
    path('courses/create/', views.course_create_edit, name='course_create'),
    path('courses/edit/<int:idCourse>', views.course_create_edit, name='course_edit'),

    #TYPEPROFESSOR ACTIONS
    path('typeprofessor/', views.typeprofessor_list, name='typeprofessor_list'),
    path('typeprofessor/create/', views.typeprofessor_create_edit, name='typeprofessor_create'),
    path('typeprofessor/edit/<int:idTypeProfessor>', views.typeprofessor_create_edit, name='typeprofessor_edit'),

    path('languages/', views.language_crud, name='language_crud'),
    path('years/', views.year_crud, name='year_crud'),
]
