"""webshell.conf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('index/', views.index),
    path('s_ture/', views.s_ture),
    # path('add/', views.drvice_add),
    path('to_data/', views.to_data),
    path('opaiai/', views.opaiai),
    path('to_reson/', views.to_reson),
    path('clean_all/', views.clean_all),
    path('drvice_true/', views.device_true),
    path('srcipt_true/', views.srcipt_true),
    path('create_input/', views.create_input),
]
