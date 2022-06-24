from django.db import models
from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.conf import settings

from HistoriasClinicas.models import Mascotas

# Create your models here.
class TipoCita(models.Model):
    tipos_citas = (
        ('Consulta', 'Consulta'),
        ('Control', 'Control'),
    )
    tipodeCita=models.CharField(max_length=45, choices=tipos_citas)

    def __str__(self):
        return self.tipodeCita

class Citas(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    mascota=models.ForeignKey(Mascotas,null=False, on_delete=models.CASCADE)
    tipo=models.ForeignKey(TipoCita,null=False, on_delete=models.CASCADE)
    asistencia = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.tipo.tipodeCita