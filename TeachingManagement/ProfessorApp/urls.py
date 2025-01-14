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
from django.urls import path
from .import views

app_name='professorapp'

urlpatterns = [
    path('', views.professor_dashboard, name='professor_dashboard'),

    path('info/', views.info_assignments, name='info_assignments'),
    path('download_info_assigments/', views.generate_assignments_pdf, name='generate_info_pdf'),

    path('details-professor/<int:professor_id>/year/<int:year_id>/',views.professor_year_assignments_summary, name='professor_details'),
    path('download_info_assigments/<int:professor_id>/year/<int:year_id>/', views.generate_professor_year_assignments_pdf, name='generate_info_pdf_given_professor'),

]
