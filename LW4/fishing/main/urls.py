"""
URL configuration for fishing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('organize_fishing/', views.organize_fishing, name='organize_fishing'),
    path('finish_fishing/', views.finish_fishing, name='finish_fishing'),
    path('process_fish/', views.process_fish, name='process_fish'),
    path('freeze_fish/', views.freeze_fish, name='freeze_fish'),
    path('transfer_to_market/', views.transfer_to_market, name='transfer_to_market'),
    path('add_ship/', views.add_ship, name='add_ship'),
    path('add_fisherman/', views.add_fisherman, name='add_fisherman'),
    path('add_net/', views.add_net, name='add_net'),
    path('logout/', views.logout, name='logout'),
]
