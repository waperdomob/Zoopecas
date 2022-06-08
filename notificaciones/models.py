from django.db import models
from django.forms import model_to_dict
from django.utils import timezone

from mascotas.models import Vacunas, dosisVacunas


class Notificaciones(models.Model):
    # 1= citas, 2= Vacunas
    notificacion_type = models.IntegerField()
    vacuna = models.ForeignKey(dosisVacunas, on_delete=models.CASCADE,null=True, blank= True)
    fecha = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)
    def __str__(self):
        return self.vacuna.mascota.nombreMas

    
