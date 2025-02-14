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

urlpatterns = [
    # use names for easy calls + functions reverse() and {% url %}  
    path('', views.home_page, name="Home"),
    path('access-denied/', views.access_denied, name='access_denied'),
]