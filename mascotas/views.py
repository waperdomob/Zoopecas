from django.shortcuts import render
import datetime
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.middleware import *
from django.views import View
from django.views.generic import CreateView,ListView, DeleteView,UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML
from django.contrib import messages
from django.shortcuts import  redirect, render

from HistoriasClinicas.models import Mascotas
from HistoriasClinicas.forms import MascotasForm


class listaMascotas(ListView):
    model = Mascotas
    
    def get(self, request, *args, **kwargs):
        mascotas = Mascotas.objects.all()
        mascota_form = MascotasForm()
        context = {'datos': mascotas,'form2':mascota_form, 'fecha_actual':datetime.date.today()}
        return render(request,'list_mascotas.html',context)

    @csrf_exempt
    def get_success_url(self):
        return reverse('HistoriasClinicas:inicio')

@login_required
def crear_Mascota(request):
    mascotas = Mascotas.objects.all()

    if request.method=="POST":
        mascota = MascotasForm(request.POST or None)
        
        if mascota.is_valid():            
            mascota.save()

        context = {'datos': mascotas,'form2':mascota, 'fecha_actual':datetime.date.today()}
        return render(request,'list_mascotas.html',context)

class UpdateMascota(UpdateView):
    model = Mascotas    
    form_class= MascotasForm
    template_name = 'mascota_editModal.html'
    success_url = reverse_lazy('mascotas_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['title'] = 'Editar Mascota'
        context['datos'] = Mascotas.objects.all()        
        return context

class deleteMascota(DeleteView):
    model = Mascotas
    template_name = 'mascota_eliminarModal.html'

    def post(self, request,pk, *args, **kwargs):        
        object = Mascotas.objects.get(id=pk)
        object.delete()
        return redirect('mascotas_list')
  

