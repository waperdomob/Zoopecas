from django.db import models
from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.conf import settings

# Create your models here.

class Categorias(models.Model):
    categoria= models.CharField(max_length=45)
    def __str__(self):
        return self.categoria

    def toJSON(self):
        item = model_to_dict(self)
        return item

class Proveedores(models.Model):
    proveedor=models.CharField(max_length=45)
    telefono = models.CharField(max_length=45)
    nombreEmpleado=models.CharField(max_length=45)

    def __str__(self):
        return self.proveedor

    def toJSON(self):
        item = model_to_dict(self)
        return item        
        
class Productos(models.Model):
    codigo=models.CharField(max_length=45,null=True, blank=True)
    producto=models.CharField(max_length=45)
    descripcion = models.CharField(max_length=100, null=True, blank=True)
    cantidad_total=models.IntegerField()
    precio_compra=models.FloatField(max_length=45)
    precio_venta=models.FloatField(max_length=20)
    imagen=models.ImageField(upload_to='productos/', null=True, blank=True)
    categoria=models.ForeignKey(Categorias,null=False, on_delete=models.CASCADE)
    proveedor=models.ForeignKey(Proveedores,null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.producto

    def toJSON(self):
        item = model_to_dict(self)
        item['precio_compra'] = format(self.precio_compra,'.2f')
        item['precio_venta'] = format(self.precio_venta,'.2f')
        item['imagen'] = self.get_image()        
        item['categoria'] = self.categoria.toJSON()
        item['proveedor'] = self.proveedor.toJSON()
        return item
    
    def get_image(self):
        if self.imagen:
            return '{}{}'.format(settings.MEDIA_URL, self.imagen)
        return '{}{}'.format(settings.STATIC_URL, 'img/gatos.png')
