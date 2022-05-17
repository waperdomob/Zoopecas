from unicodedata import name
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.urls import path,include
from django.urls import re_path
from HistoriasClinicas import views
from .views import create_Propietario, create_Mascota,new_HC,create_HC,create_seguimiento

urlpatterns = [
       
    path('',views.index, name='inicio'),
    re_path('^ajax_search/$', views.ajax_search, name='ajax_search'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('historiaClinica/',login_required(views.crearHistoriaC.as_view()), name='historiaClinica'),
    path('historiaClinica/edit/<int:pk>/',login_required(views.HCUpdate.as_view()), name='editarHC'),
    path('historiaClinica/Detalle/<int:pk>/',login_required(views.HCDetailView.as_view()), name='detalleHC'),
    path('savePropietario/', create_Propietario, name='create_Propietario'),
    path('saveMascota/', create_Mascota, name='create_Mascota'),
    path('saveSeguimiento/<int:pk>', create_seguimiento, name='create_seguimiento'),
    path('saveHistoriaClinica/', create_HC, name='saveHistoriaClinica'),
    path('nuevaHistoriaClinica/', new_HC, name='nuevaHistoriaClinica'),

]