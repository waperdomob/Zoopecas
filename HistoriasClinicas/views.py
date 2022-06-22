
import datetime as dtime
from datetime import datetime,  timedelta
from threading import Thread
from time import sleep
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.middleware import *
from django.views import View
from django.views.generic import CreateView,ListView, DetailView,UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.http import  HttpResponseRedirect, JsonResponse
import os
from Veterinaria.wsgi import *
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML
from django.contrib import messages
from django.shortcuts import  redirect, render

from HistoriasClinicas.forms import HistoriasCForm, MascotasForm, PropietariosForm, SearchForm, SeguimientoForm
from HistoriasClinicas.models import Propietarios, HistoriasClinicas, Seguimiento
from mascotas.models import dosisVacunas
from Veterinaria.settings import STATIC_URL
from notificaciones.models import Notificaciones
# Create your views here.

class Temporizador(Thread):
    def __init__(self, hora, delay, funcion):
        # El constructor recibe como parámetros:
        ## hora = en un string con formato hh:mm:ss y es la hora a la que queremos que se ejecute la función.
        ## delay = tiempo de espera entre comprobaciones en segundos.
        ## funcion = función a ejecutar.
        super(Temporizador, self).__init__()
        self._estado = True
        self.hora = hora
        self.delay = delay
        self.funcion = funcion

    def stop(self):
        self._estado = False

    def run(self):
        # Pasamos el string a dato tipo datetime
        aux = datetime.strptime(self.hora, '%H:%M:%S')
        # Obtenemos la fecha y hora actuales.
        hora = datetime.now()
        # Sustituimos la hora por la hora a ejecutar la función.
        hora = hora.replace(hour = aux.hour, minute=aux.minute, second=aux.second, microsecond = 0)
        # Comprobamos si la hora ya a pasado o no, si ha pasado sumamos un dia (hoy ya no se ejecutará).
        if hora <= datetime.now():
            hora += timedelta(days=1)

        # Iniciamos el ciclo:
        while self._estado:
            if hora <= datetime.now():
                self.funcion()
                hora += timedelta(days=1)
            sleep(self.delay)

def ejecutar():
    d = dtime.date.today() - timedelta(days=3)
    notificaciones = Notificaciones.objects.filter(Q(user_has_seen=True),fecha__range=[d,dtime.date.today()])
    for notificacion in notificaciones:
        if notificacion.vacuna.fecha_sgt_dosis <= dtime.date.today():
            print(notificacion.user_has_seen)
            notificacion.user_has_seen = False
            notificacion.save()

def index(request):
    if request.user.is_authenticated:
        hora = datetime.now()
        if str(hora.time()) >="14:50:00" and str(hora.time())<="14:57:00":
            t = Temporizador('14:57:00',1,ejecutar)# Instanciamos nuestra clase Temporizador
            t.start() #Iniciamos el hilo
            print(hora.time())
             # Si en cualquier momento queremos detener el hilo desde la aplicacion simplemete usamos el método stop()
            sleep(60) # Simulamos un tiempo de espera durante el cual el programa principal puede seguir funcionando. 
            t.stop()   # Detenemos el hilo.
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
        context = {'datos': historiasClinicas,'form2':seguimiento, 'fecha_actual':dtime.date.today()}
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
        context['fecha_actual'] =dtime.date.today()
        context['Hora_actual'] = dtime.datetime.now().time()
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
        context['seguimientos'] = Seguimiento.objects.filter(historiaClinica_id=self.kwargs['pk'])
                
        return context
   
class HistoriaClinicaPDF(View):
    
    def get(self, request, *args, **kwargs):
        try:
            template = get_template('hcPDF.html')
            context = {
                'object': HistoriasClinicas.objects.get(pk=self.kwargs['pk']),
                'seguimientos':Seguimiento.objects.filter(historiaClinica_id=self.kwargs['pk']),
                'icon' : '{}{}'.format(STATIC_URL, 'img/veterinariaHC.jpg')
            }
            html_template = template.render(context)
            pdf = HTML(string=html_template, base_url= request.build_absolute_uri('/')).write_pdf()
            return HttpResponse(pdf, content_type= 'application/pdf')
            
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('historiaClinica'))


        
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

        context = {'form':historiasClinicas, 'fecha_actual':dtime.date.today(),'Hora_actual': dtime.datetime.now().time()}
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
        context = {'datos': historiasClinicas,'form2':seguimiento, 'fecha_actual':dtime.date.today()}
        return render(request,'indexHC.html',context)

    
@login_required
def new_HC(request):
    historiasClinicas = HistoriasCForm()

    context = {'form':historiasClinicas,'fecha_actual':dtime.date.today(),'Hora_actual': dtime.datetime.now().time()}
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
        context = {'datos': historiasClinicas, 'fecha_actual':dtime.date.today()}
        return render(request,'indexHC.html',context)

    