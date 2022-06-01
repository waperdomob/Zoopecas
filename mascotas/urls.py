from unicodedata import name
from django.contrib.auth.decorators import login_required
from django.urls import path,include
from django.urls import re_path
from mascotas import views
from .views import *

urlpatterns = [
       
    path('mascotas/',login_required(views.listaMascotas.as_view()), name='mascotas_list'),
    path('saveMascota/', crear_Mascota, name='crear_Mascota'),
    path('mascota/eliminar/<int:pk>/',login_required(views.deleteMascota.as_view()), name='eliminar_mascota'),
    path('mascota/edit/<int:pk>/',login_required(views.UpdateMascota.as_view()), name='editar_mascota'),

]