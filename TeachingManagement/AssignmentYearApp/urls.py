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
    path('check-section/', views.check_section_chief_section, name='test_sectionchief'),

    #For the COURSES
    path('section-courses/', views.section_courses_list, name='section_courses_list'),
    path('section-courses/show/<int:idCourseYear>/', views.courseyear_show, name='courseyear_show'),

        #For updating only the comment in a CourseYear
    path('update-course-year-comment/<int:idCourseYear>/', views.update_course_year_comment, name='update_course_year_comment'),
        #modifyning the points of a professor Assigned in a Course Year
    path('update-assignment/<int:idAssignment>/', views.update_assignment, name='update_assignment'),
    path('get-assignment/<int:assignment_id>/', views.get_assignment, name='get-assignment'),


    path('delete_professor/<int:idProfessor>/<int:idCourseYear>/', views.delete_courseyear_professor, name='delete_courseyear_professor'),

]
