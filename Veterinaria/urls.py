"""Veterinaria URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls import handler404
from HistoriasClinicas.views import page_not_found404
 
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('',include('HistoriasClinicas.urls')),
    path('',include('Inventario.urls')),
    path('',include('Clientes.urls')),
    path('',include('Ventas.urls')),
    path('',include('reportes.urls')),
    path('',include('mascotas.urls')),
    path('',include('notificaciones.urls')),
    path('',include('citas.urls')),

]
handler404 = page_not_found404