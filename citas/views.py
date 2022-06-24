from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required

from citas.forms import CitasForm
from citas.models import Citas
from notificaciones.models import Notificaciones
# Create your views here.


@login_required
def citasCreate(request):
    
    if request.method=="POST":
        citas = CitasForm(request.POST or None)
        if citas.is_valid():            
            newcita = citas.save(commit=False)
            newcita.save()        
            Notificaciones.objects.create(notificacion_type=1, cita = newcita, fecha= newcita.fecha )
            print("Hola ")
        return redirect('inicio')

    else:
        return redirect('inicio')