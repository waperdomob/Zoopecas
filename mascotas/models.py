from django.db import models
from django.forms import model_to_dict

from HistoriasClinicas.models import HistoriasClinicas,Mascotas
# Create your models here.

class Vacunas(models.Model):
    vacuna = models.CharField(max_length=45)
    cantidad = models.IntegerField()
    dosis = models.IntegerField()
    
    def __str__(self):
        return self.vacuna

    
class dosisVacunas(models.Model):
    dosis_aplicada = models.IntegerField()
    fecha_aplicacion = models.DateField(auto_now_add=True)
    mascota = models.ForeignKey(Mascotas,null=True, on_delete=models.CASCADE)
    vacuna = models.ForeignKey(Vacunas,null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.dosis_aplicada