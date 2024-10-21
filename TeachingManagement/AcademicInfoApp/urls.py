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
    path('fields/', views.field_crud, name='field_crud'),
    path('sections/', views.section_crud, name='section_crud'),
    path('schools/', views.school_crud, name='school_crud'),
    path('degrees/', views.degree_crud, name='degree_crud'),
    path('courses/', views.course_crud, name='courses_crud'),
    path('typeprofessor/', views.type_professor_crud, name='type_professor_crud'),
    path('languages/', views.language_crud, name='language_crud'),
    path('years/', views.year_crud, name='year_crud'),
]
