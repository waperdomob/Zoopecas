from django.contrib import admin

from Ventas import *
from Ventas.models import Venta, DetVenta, MetodoPagos
# Register your models here.

class metodosPagoAdmin(admin.ModelAdmin):
    list_display=("metodoPago",)

class ventaAdmin(admin.ModelAdmin):
    list_display=("cliente","metodoPago","fecha_compra","subtotal","descuento","total",)

class detalleVentaAdmin(admin.ModelAdmin):
    list_display=("venta","producto","precio","cant","subtotal",)

admin.site.register(MetodoPagos,metodosPagoAdmin)
admin.site.register(Venta,ventaAdmin)
admin.site.register(DetVenta,detalleVentaAdmin)