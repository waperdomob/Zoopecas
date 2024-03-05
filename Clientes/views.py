from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView,ListView, UpdateView,DeleteView,DetailView

from HistoriasClinicas.models import  Mascotas, Propietarios
from Clientes.forms import ClientesForm
from HistoriasClinicas.forms import MascotasForm



# Create your views here.

class clienteDetailView(PermissionRequiredMixin,DetailView):
    permission_required = 'HistoriasClinicas.view_propietarios'
    model = Propietarios
    template_name='detalleCliente.html'

    def get_queryset(self):
        qs = super(clienteDetailView, self).get_queryset()
        return qs.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mascotas'] = Mascotas.objects.filter(propietario_id=self.kwargs['pk'])
        context['mascota_form']  = MascotasForm(initial={'propietario': self.kwargs['pk'] }) 
        return context
   
class registrarCliente(CreateView):
    model = Propietarios    
    form_class= ClientesForm
    template_name = 'cliente_Modal.html'
    success_url = reverse_lazy('clientes')

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):        
        context = {}
        context['title'] = 'REGISTRAR CLIENTE'
        context['clientes'] = self.get_queryset()
        context['form'] = self.form_class
        return context

    def get(self, request, *args, **kwargs):        
        return render(request,self.template_name,self.get_context_data())

class listaClientes(PermissionRequiredMixin,ListView):
    permission_required = 'HistoriasClinicas.view_propietarios'
    model = Propietarios    
    form_class= ClientesForm
    template_name = 'clientes.html'
    

    def get_queryset(self):
        return self.model.objects.get_queryset().order_by('id')

    def get_context_data(self,*args, **kwargs):        
        context = {}
        context['title'] = 'LISTA DE CLIENTES'
        context['clientes'] = self.get_queryset()
        context['form'] = self.form_class
        return context

    def get(self, request, *args, **kwargs):              
        return render(request,self.template_name,self.get_context_data())

class ClienteUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = 'HistoriasClinicas.change_propietarios'
    model = Propietarios
    form_class = ClientesForm
    template_name = 'cliente_editModal.html'
    success_url = reverse_lazy('clientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['title'] = 'Editar Cliente'
        context['clientes'] = Propietarios.objects.all()        
        return context

class deleteCliente(PermissionRequiredMixin,DeleteView):
    permission_required = 'HistoriasClinicas.delete_propietarios'
    model = Propietarios
    template_name = 'cliente_eliminarModal.html'

    def post(self, request,pk, *args, **kwargs):        
        object = Propietarios.objects.get(id=pk)
        object.delete()
        return redirect('clientes')
 

@login_required
def agregar_Mascota(request):
   
    if request.method=="POST":
        mascota = MascotasForm(request.POST or None)
        
        if mascota.is_valid():            
            mascota.save()

        return redirect('clientes')
        