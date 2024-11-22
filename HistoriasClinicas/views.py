
import datetime as dtime
from datetime import datetime,  timedelta
from threading import Thread
from time import sleep
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.middleware import *
from django.views import View
from django.views.generic import CreateView, ListView, DetailView,  DeleteView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.http import  HttpResponseRedirect, JsonResponse
import os
from Veterinaria.wsgi import *
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML
from django.contrib import messages
from django.shortcuts import  get_object_or_404, redirect, render

from HistoriasClinicas.forms import DocumentosForm, HistoriasCForm, MascotasForm, PropietariosForm, SearchForm, SeguimientoForm
from HistoriasClinicas.models import Documento, Mascotas, Propietarios, HistoriasClinicas, Seguimiento
from Veterinaria.settings import STATIC_URL
from citas.forms import CitasForm
from citas.models import Citas
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
        aux = datetime.strptime(self.hora, '%H:%M')
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
        if notificacion.vacuna.fecha_sgt_dosis >= dtime.date.today():
            notificacion.user_has_seen = False
            notificacion.save()
        if notificacion.cita.fecha >= dtime.date.today():
            notificacion.user_has_seen = False
            notificacion.save()

def index(request):
    if request.user.is_authenticated:
        hora = datetime.now()
        if str(hora.time()) >="09:00:00" and str(hora.time())<="09:10:00":
            t = Temporizador('09:05',1,ejecutar)# Instanciamos nuestra clase Temporizador
            t.start() #Iniciamos el hilo
            print(hora.time())
             # Si en cualquier momento queremos detener el hilo desde la aplicacion simplemete usamos el método stop()
            sleep(60) # Simulamos un tiempo de espera durante el cual el programa principal puede seguir funcionando. 
            t.stop()   # Detenemos el hilo.
        mascota = MascotasForm()
        propietario = PropietariosForm() 
        datos = Citas.objects.all().order_by('id')
        form = SearchForm()
        formCita = CitasForm()       
        return render(request, 'consultarProp.html', {'citas':datos,'form': form, 'form2':mascota,'form3':propietario,'formCita':formCita,'cliente': False, })
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
        historiasC = HistoriasClinicas.objects.filter(is_active=True).all()
        page = request.GET.get('page',1)
        pag = Paginator(historiasC,10)
        historiasClinicas = pag.get_page(page)
        page_range_to_show = 5  # Puedes ajustar este valor según tus necesidades
        current_page = historiasClinicas.number
        start_page = max(1, current_page - page_range_to_show // 2)
        end_page = min(pag.num_pages, current_page + page_range_to_show // 2)
        page_range = range(start_page, end_page + 1)
        seguimiento = SeguimientoForm()
        context = {'datos': historiasClinicas, 'page_range': page_range,'form2':seguimiento, 'fecha_actual':dtime.date.today()}
        return render(request,'indexHC.html',context)

    @csrf_exempt
    def get_success_url(self):
        return reverse('HistoriasClinicas:inicio')


class HCUpdate(UpdateView):
    model = HistoriasClinicas
    form_class = HistoriasCForm
    template_name = 'editHc.html'
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
    template_name = 'detalleHC.html'

    def get_queryset(self):
        qs = super(HCDetailView, self).get_queryset()
        return qs.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seguimientos'] = Seguimiento.objects.filter(historiaClinica_id=self.kwargs['pk'])
        context['documentos'] = Documento.objects.filter(historia_clinica=self.object)

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

    if request.method=="POST":
        mascota = MascotasForm(request.POST or None)
        
        if mascota.is_valid():            
            mascota.save()
        last_mascota = Mascotas.objects.all().last()
        historiasClinicas = HistoriasCForm(initial={ 'mascotas': last_mascota})

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
    documentosForm = DocumentosForm()
    context = {'form':historiasClinicas, 'doc_form':documentosForm, 'fecha_actual':dtime.date.today(),'Hora_actual': dtime.datetime.now().time()}
    return  render(request,'formulario.html',context)

@login_required
def create_HC(request):

    if request.method=="POST":
        historiaClinica = HistoriasCForm(request.POST)
        documentosForm = DocumentosForm(request.POST, request.FILES)
        if historiaClinica.is_valid() and documentosForm.is_valid():            
            historia_clinica = historiaClinica.save()

            # Guardar cada documento
            archivos = request.FILES.getlist('archivos')
            if archivos:
                print(f"Archivos recibidos: {[archivo.name for archivo in archivos]}") 
                for archivo in archivos:
                    Documento.objects.create(
                        historia_clinica=historia_clinica,
                        archivo=archivo,
                        titulo=archivo.name  # Usar el nombre del archivo para el título
                    )
            else:
                print("No se recibieron archivos.") 
        else:
            print(f"Errores del formulario HistoriaClinica: {historiaClinica.errors}")
            print(f"Errores del formulario Documentos: {documentosForm.errors}")
            messages.error(request, "Hubo un error al guardar la historia clinica, intenta nuevamente")

        historiasClinicas = HistoriasClinicas.objects.all()        
        context = {'datos': historiasClinicas, 'fecha_actual':dtime.date.today()}
        return render(request,'indexHC.html',context)

def page_not_found404(request, exception):

    return render(request,'404.html')

class CreateSeguimiento(CreateView):
    model = Seguimiento
    form_class = SeguimientoForm
    template_name = 'seguimientoCreate.html'
    success_url = reverse_lazy('historiaClinica')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Seguimiento de Historia Clinica'
        context['historia_clinica'] = get_object_or_404(HistoriasClinicas, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        historia_clinica_id = self.kwargs['pk']
        historia_clinica = get_object_or_404(HistoriasClinicas, pk=historia_clinica_id)
        form.instance.historiaClinica = historia_clinica
        form.save()
        # Redireccionar a la URL 'detalleHC' con el ID de la historia clínica
        return HttpResponseRedirect(reverse('detalleHC', args=[historia_clinica_id]))

class UpdateSeguimiento(UpdateView):
    model = Seguimiento
    form_class = SeguimientoForm
    template_name = 'seguimientoEdit.html'
    success_url = reverse_lazy('historiaClinica')

    def get_success_url(self):
        historia_clinica_id = self.object.historiaClinica_id
        return reverse('detalleHC', kwargs={'pk': historia_clinica_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Seguimiento de Historia Clinica'
        context['datos'] = Seguimiento.objects.all()   
        return context

class DeleteSeguimiento(DeleteView):
    model = Seguimiento
    template_name = 'Seguimiento_eliminarModal.html'

    def post(self, request,pk, *args, **kwargs):        
        object = Seguimiento.objects.get(id=pk)
        object.delete()
        return redirect('historiaClinica')