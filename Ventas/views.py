import json
from django.db import transaction
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView,UpdateView,DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from Ventas.forms import VentasForm
from Ventas.models import Venta, DetVenta
from Inventario.models import Productos
# Create your views here.

class SaleListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Venta
    template_name = 'venta/list.html'
    permission_required = 'venta.view_sale'
    paginate_by = 2

    def get_queryset(self):
        return self.model.objects.get_queryset().order_by('id')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Venta.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in DetVenta.objects.filter(venta_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = {}
        context['title'] = 'Listado de Ventas'
        context['ventas'] = self.get_queryset()
        context['create_url'] = reverse_lazy('venta_create')
        context['list_url'] = reverse_lazy('venta_list')
        return context

    def get(self, request, *args, **kwargs):              
        return render(request,self.template_name,self.get_context_data())


class SaleCreateView(LoginRequiredMixin, CreateView):
    model = Venta
    form_class = VentasForm
    template_name = 'venta/create.html'
    success_url = reverse_lazy('venta_create')
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                products = Productos.objects.filter(producto__icontains=request.POST['term'])[0:10]
                for i in products:
                    item = i.toJSON()
                    item['value'] = i.producto
                    data.append(item)
            elif action == 'search_autocomplete':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text': term})
                products = Productos.objects.filter(producto__icontains=term, cantidad_total__gt=0)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.producto
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    venta = Venta()
                    venta.fecha_compra = vents['fecha_compra']
                    venta.cliente_id = vents['cliente']
                    venta.metodoPago_id = vents['metodoPago']
                    venta.subtotal = float(vents['subtotal'])
                    venta.descuento = float(vents['descuento'])
                    venta.total = float(vents['total'])
                    venta.save()

                    for i in vents['productos']:
                        detalle = DetVenta()
                        detalle.venta_id = venta.id
                        detalle.producto_id = i['id']
                        detalle.cant = int(i['cant'])
                        detalle.precio = float(i['precio_venta'])
                        detalle.subtotal = float(i['subtotal'])
                        detalle.save()
                        cantidad_ActualP = Productos.objects.filter(pk = i['id']).values_list('cantidad_total',flat=True)
                        cantidad_ActualP = int(cantidad_ActualP[0])
                        cantidad_ActualP = cantidad_ActualP - detalle.cant
                        Productos.objects.filter(id = i['id']).update(cantidad_total = cantidad_ActualP)
            
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Venta'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['detalle'] = []

        return context

class SaleEditView(UpdateView):
    model = Venta    
    form_class= VentasForm
    template_name = 'venta/create.html'
    success_url = reverse_lazy('venta_list')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                products = Productos.objects.filter(producto__icontains=request.POST['term'])[0:10]
                for i in products:
                    item = i.toJSON()
                    item['value'] = i.producto
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    venta = self.get_object()
                    venta.fecha_compra = vents['fecha_compra']
                    venta.cliente_id = vents['cliente']
                    venta.metodoPago_id = vents['metodoPago']
                    venta.subtotal = float(vents['subtotal'])
                    venta.descuento = float(vents['descuento'])
                    venta.total = float(vents['total'])
                    venta.save()
                    venta.detventa_set.all().delete()
                    for i in vents['productos']:
                        detalle = DetVenta()
                        detalle.venta_id = venta.id
                        detalle.producto_id = i['id']
                        detalle.cant = int(i['cant'])
                        detalle.precio = float(i['precio_venta'])
                        detalle.subtotal = float(i['subtotal'])
                        detalle.save()
                        """ cantidad_ActualP = Productos.objects.filter(pk = i['id']).values_list('cantidad_total',flat=True)
                        cantidad_ActualP = int(cantidad_ActualP[0])
                        cantidad_compra = int(i['cant'])
                        cantidad_ActualP = cantidad_ActualP - cantidad_compra
                        Productos.objects.filter(id = i['id']).update(cantidad_total = cantidad_ActualP) """
            
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_product(self):
        data = []
        try:
            for i in DetVenta.objects.filter(venta=self.kwargs['pk']):
                item = i.producto.toJSON()
                item['cant'] = i.cant
                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Venta'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['detalle'] = json.dumps(self.get_details_product())
        return context

class SaleDeleteView(DeleteView):
    model = Venta
    template_name = 'venta/delete.html'
    success_url = reverse_lazy('venta_list')
    url_redirect = success_url

    def post(self, request,pk, *args, **kwargs):        
        object = Venta.objects.get(id=pk)
        object.delete()
        return redirect('venta_list')