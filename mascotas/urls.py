from unicodedata import name
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.urls import path,include
from django.urls import re_path
from mascotas import views
from .views import *

urlpatterns = [
       
    path('mascotas/',login_required(views.listaMascotas.as_view()), name='mascotas_list'),
    path('mascotas/detalleMascota/<int:pk>/',login_required(views.mascotaDetailView.as_view()), name='detalleMascota'),
    path('saveMascota/', crear_Mascota, name='crear_Mascota'),
    path('mascota/eliminar/<int:pk>/',login_required(views.deleteMascota.as_view()), name='eliminar_mascota'),
    path('mascota/edit/<int:pk>/',login_required(views.UpdateMascota.as_view()), name='editar_mascota'),
    path('vacunacion/<int:pk>', registrarVacuna, name='vacunacion'),
    path('mascota/editarVacuna/<int:pk>', login_required(views.vacunaUpdate.as_view()), name='editarVacuna'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)