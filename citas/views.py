from datetime import datetime
from django.http import HttpResponseRedirect
import pandas as pd
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView,UpdateView
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

class CitaUpdate(UpdateView):
    model = Citas
    form_class = CitasForm
    template_name = 'cita_editModal.html'
    success_url = reverse_lazy('mascotas_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        fechaN =form['fecha'].value()
        if (form.is_valid() ):
            Notificaciones.objects.create(notificacion_type=1, cita = self.object, fecha = fechaN)

            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()        
        return HttpResponseRedirect(self.get_success_url())