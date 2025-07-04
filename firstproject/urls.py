"""
URL configuration for firstproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
#要用這個重整 python manage.py runserver
from django.contrib import admin
from django.urls import path
from myapp.views import sayhello   #自己的模組
from myapp.views import homepage, get_era_from_mlb, get_pitcher_win_loss
from myapp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',homepage),
    path('hello', sayhello),  #index的概念
    path('api/era/', get_era_from_mlb, name='get_era_data'),
    path('api/WL/', get_pitcher_win_loss, name='get_WL_data'),
    #path('listone/', views.listone),
    #path('listall/', views.listall),
    #path('index/', views.index),
]
