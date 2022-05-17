from unicodedata import name
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.urls import path,include
from django.contrib.auth.decorators import login_required

from HistoriasClinicas import views
from Clientes import views

urlpatterns = [
    path('registrarCliente/',login_required(views.registrarCliente.as_view()), name='registrarCliente'),
    path('clientes/',login_required(views.listaClientes.as_view()), name='clientes'),
    path('clientes/eliminar/<int:pk>/',login_required(views.deleteCliente.as_view()), name='eliminarCliente'),
    path('clientes/edit/<int:pk>/',login_required(views.ClienteUpdate.as_view()), name='editarCliente'),
   

]