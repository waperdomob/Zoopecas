from django.shortcuts import render
import datetime
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.middleware import *
from django.views import View
from django.views.generic import DetailView,ListView, DeleteView,UpdateView
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import  redirect, render

from HistoriasClinicas.models import Mascotas,HistoriasClinicas
from HistoriasClinicas.forms import MascotasForm
from notificaciones.models import Notificaciones
from .models import Vacunas,dosisVacunas
from .forms import dosisVacunasForm

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


class mascotaDetailView(DetailView):

    model = Mascotas
    template_name='detalleMascota.html'

    def get_queryset(self):
        qs = super(mascotaDetailView, self).get_queryset()
        return qs.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacunas'] = dosisVacunas.objects.filter(mascota_id=self.kwargs['pk'])
        context['historiaClinica'] = HistoriasClinicas.objects.filter(mascotas_id=self.kwargs['pk'])
        context['formVacuna']  = dosisVacunasForm()  
        return context
   
@login_required
def crear_Mascota(request):
    mascotas = Mascotas.objects.all()

    if request.method=="POST":
        mascota = MascotasForm(request.POST or None)
        
        if mascota.is_valid():            
            mascota.save()

        context = {'datos': mascotas,'form2':mascota, 'fecha_actual':datetime.date.today()}
        return render(request,'list_mascotas.html',context)
        
@login_required
def registrarVacuna(request, pk):
    mascota = Mascotas.objects.filter(id = pk)

    if request.method=="POST":
        vacunaAplicada = dosisVacunasForm(request.POST or None)
        if vacunaAplicada.is_valid():            
            newdosis = vacunaAplicada.save(commit=False)
            newdosis.mascota_id = pk
            vacunaAplicada.save()        
            Notificaciones.objects.create(notificacion_type=2, vacuna = newdosis, fecha = newdosis.fecha_sgt_dosis)

        return redirect('detalleMascota',pk)

    else:
        return redirect('detalleMascota',pk)

class vacunaUpdate(UpdateView):
    model = dosisVacunas
    form_class = dosisVacunasForm
    template_name = 'vacunaEditModal.html'
    success_url = reverse_lazy('mascotas_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Notificaciones.objects.create(notificacion_type=2, vacuna = context['dosisvacunas'])
        return context

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
  

