from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.db.models import FloatField, F


def agregarData(consulta):
    data = []
    for i in consulta:
        data.append([
        i.venta.id,
        i.producto.producto,
        i.venta.fecha_compra.strftime('%Y-%m-%d'),
        i.venta.metodoPago.metodoPago,
        format(i.subtotal, '.2f'),
        format(i.venta.descuento, '.2f'),
        format(i.subtotal,'.2f'),
    ])

    subtotal_sum = consulta.aggregate(r=Coalesce(Sum(F('subtotal')),0,output_field=FloatField())).get('r')
    descuento_sum = 0
    total_sum = consulta.aggregate(r=Coalesce(Sum(F('subtotal')),0,output_field=FloatField())).get('r')
    data.append([
        '-----',
        '-----',
        '-----',
        '-----',
        format(subtotal_sum, '.2f'),
        format(descuento_sum, '.2f'),
        format(total_sum,'.2f'),
    ]) 
    return data