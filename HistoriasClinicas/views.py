
import datetime
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.middleware import *
from django.views.generic import CreateView,ListView, DetailView,UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.http import  JsonResponse

from django.contrib import messages
from django.shortcuts import  redirect, render

from HistoriasClinicas.forms import HistoriasCForm, MascotasForm, PropietariosForm, SearchForm, SeguimientoForm
from HistoriasClinicas.models import Propietarios, HistoriasClinicas, Seguimiento

# Create your views here.

def index(request):   
    if request.user.is_authenticated:
        mascota = MascotasForm()
        propietario = PropietariosForm()        
        form = SearchForm()

        return render(request, 'consultarProp.html', {'form': form, 'form2':mascota,'form3':propietario,'cliente': False, })
    else:    
        response = redirect('/accounts/login')
        return response

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def ajax_search(request):
    if is_ajax(request=request):
        if request.method == 'GET':
            documento = None
            nombrePr = None
            id = None
            identificacion = request.GET.get('documento')
            if identificacion:
                cliente = Propietarios.objects.filter(documentoid=identificacion)
                for item in cliente:
                    id = item.id
                    documento = item.documentoid
                    nombrePr = item.nombrePr
                data = {"cliente": nombrePr,"documento":documento, "id":id}
                return JsonResponse(data)
            else:                
                return JsonResponse()
                
class crearHistoriaC(ListView):
    model = HistoriasClinicas
    
    def get(self, request, *args, **kwargs):
        historiasClinicas = HistoriasClinicas.objects.all()
        seguimiento = SeguimientoForm()
        context = {'datos': historiasClinicas,'form2':seguimiento, 'fecha_actual':datetime.date.today()}
        return render(request,'indexHC.html',context)

    @csrf_exempt
    def get_success_url(self):
        return reverse('HistoriasClinicas:inicio')


class HCUpdate(UpdateView):
    model = HistoriasClinicas
    form_class = HistoriasCForm
    template_name = 'editHC.html'
    success_url = reverse_lazy('historiaClinica')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['title'] = 'Editar Historia Clinica'
        context['entity'] = 'HistoriasClinicas'
        context['list_url'] = reverse_lazy('historiaClinica')
        context['fecha_actual'] =datetime.date.today()
        context['Hora_actual'] = datetime.datetime.now().time()
        context['historiasC'] = HistoriasClinicas.objects.all()        
        return context

class HCDetailView(DetailView):

    model = HistoriasClinicas
    template_name='detalleHC.html'
    def get_queryset(self):
        qs = super(HCDetailView, self).get_queryset()
        return qs.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context
   

@login_required
def create_Propietario(request):
    mascota = MascotasForm()
    propietario = PropietariosForm()        
    form = SearchForm()
    if request.method=="POST":
        cliente = PropietariosForm(request.POST or None)
        
        if cliente.is_valid():            
            cliente.save()

        return render(request, 'consultarProp.html', {'form': form, 'form2':mascota,'form3':propietario,'cliente': False, })
        
@login_required
def create_Mascota(request):
    historiasClinicas = HistoriasCForm()

    if request.method=="POST":
        mascota = MascotasForm(request.POST or None)
        
        if mascota.is_valid():            
            mascota.save()

        context = {'form':historiasClinicas, 'fecha_actual':datetime.date.today(),'Hora_actual': datetime.datetime.now().time()}
        return  render(request,'formulario.html',context)

@login_required
def create_seguimiento(request,pk):   

    if request.method=="POST":
        seguimiento = SeguimientoForm(request.POST or None)
        
        if seguimiento.is_valid():            
            newSeguimiento = seguimiento.save(commit=False)
            newSeguimiento.historiaClinica_id = pk
            newSeguimiento.save()
            return redirect('historiaClinica')#redirigue a donde deseas

    else:
        historiasClinicas = HistoriasClinicas.objects.all()
        seguimiento = SeguimientoForm()
        context = {'datos': historiasClinicas,'form2':seguimiento, 'fecha_actual':datetime.date.today()}
        return render(request,'indexHC.html',context)

@login_required
def ver_seguimientos(request,pk):   

    seguimiento = Seguimiento.objects.filter(historiaClinica_id = pk)    
    return redirect('historiaClinica')#redirigue a donde deseas

    
@login_required
def new_HC(request):
    historiasClinicas = HistoriasCForm()

    context = {'form':historiasClinicas,'fecha_actual':datetime.date.today(),'Hora_actual': datetime.datetime.now().time()}
    return  render(request,'formulario.html',context)

@login_required
def create_HC(request):

    if request.method=="POST":
        formulario = HistoriasCForm(request.POST)
        if formulario.is_valid():            
            formulario.save()
        else:
            messages.error(request, "Hubo un error al guardar la historia clinica, intenta nuevamente")

        historiasClinicas = HistoriasClinicas.objects.all()        
        context = {'datos': historiasClinicas, 'fecha_actual':datetime.date.today()}
        return render(request,'indexHC.html',context)

    