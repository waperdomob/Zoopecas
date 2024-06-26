from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.views.generic import TemplateView
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.db.models import FloatField, F

from reportes.funciones.funciones import *
from reportes.forms import reportForm
from Ventas.models import Venta, DetVenta

# Create your views here.
class ReportVentasView(PermissionRequiredMixin,TemplateView):
    permission_required = 'Ventas.view_venta'
    template_name= 'reportes.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date= request.POST.get('start_date','')
                end_date= request.POST.get('end_date','')
                metodo_pago = request.POST.get('metodo_pago','')
                categoria = request.POST.get('categoria','')

                search = Venta.objects.all()
                search2 = DetVenta.objects.all()
               
                if metodo_pago:
                    if metodo_pago != "0":
                        consulta = search.filter(fecha_compra__range=[start_date,end_date]).filter(metodoPago=metodo_pago)
                    elif metodo_pago == "0":
                        consulta = search.filter(fecha_compra__range=[start_date,end_date])
                elif categoria:
                    if categoria != "0":
                        consulta2 = search2.select_related('venta').filter(producto__categoria = categoria).filter(venta__fecha_compra__range=[start_date,end_date]) 
                       
                        data = agregarData(consulta2)    
                        return JsonResponse(data, safe=False)

                    elif categoria == "0":
                        consulta = search.filter(fecha_compra__range=[start_date,end_date])
                else:
                    consulta = search.filter(fecha_compra__range=[start_date,end_date])   
                for i in consulta:
                    data.append([
                        i.id,
                        i.cliente.nombrePr,
                        i.fecha_compra.strftime('%Y-%m-%d'),
                        i.metodoPago.metodoPago,
                        format(i.subtotal, '.2f'),
                        format(i.descuento, '.2f'),
                        format(i.total,'.2f'),
                    ])
                subtotal_sum = consulta.aggregate(r=Coalesce(Sum(F('subtotal')),0,output_field=FloatField())).get('r')
                descuento_sum = consulta.aggregate(r=Coalesce(Sum(F('descuento')),0,output_field=FloatField())).get('r')
                total_sum = consulta.aggregate(r=Coalesce(Sum(F('total')),0,output_field=FloatField())).get('r')
                 
                data.append([
                    '-----',
                    '-----',
                    '-----',
                    '-----',
                    format(subtotal_sum, '.2f'),
                    format(descuento_sum, '.2f'),
                    format(total_sum,'.2f'),
                ])    
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Ventas'
        context['list_url'] = reverse_lazy('reporte_ventas')
        context['form'] = reportForm()
        return context