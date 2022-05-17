from asyncio.windows_events import NULL
from pickle import TRUE
from django.db import models
from datetime import datetime
from django.forms import model_to_dict

from HistoriasClinicas.models import Propietarios
from Inventario.models import  Productos
# Create your models here.


class MetodoPagos(models.Model):
    metodoPago= models.CharField(max_length=45)
    def __str__(self):
        return self.metodoPago
    def toJSON(self):
        item = model_to_dict(self)

class Venta(models.Model):
    cliente = models.ForeignKey(Propietarios, on_delete=models.CASCADE)
    metodoPago = models.ForeignKey(MetodoPagos, on_delete=models.CASCADE)
    fecha_compra = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    descuento = models.DecimalField(default=0.00 , null=True, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.cliente.nombrePr

    def toJSON(self):
        item = model_to_dict(self)
        item['cliente'] = self.cliente.toJSON()
        item['metodoPago'] = self.metodoPago.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['descuento'] = format(self.descuento, '.2f')
        item['total'] = format(self.total, '.2f')
        item['fecha_compra'] = self.fecha_compra.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']


class DetVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.producto.producto

    def toJSON(self):
        item = model_to_dict(self, exclude=['venta'])
        item['producto'] = self.producto.toJSON()
        item['precio'] = format(self.precio, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        ordering = ['id']

