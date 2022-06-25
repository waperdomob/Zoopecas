from django.contrib.auth.decorators import login_required
from django.urls import path,include
from citas import views
from .views import *

urlpatterns = [
        path('citas/nuevaCita/', citasCreate, name='asignarCita'),
        path('citas/edit/<int:pk>/',login_required(views.CitaUpdate.as_view()), name='editarCita'),

]