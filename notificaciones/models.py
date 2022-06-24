from django.db import models
from django.forms import model_to_dict
from django.utils import timezone

from citas.models import Citas
from mascotas.models import Vacunas, dosisVacunas


class Notificaciones(models.Model):
    # 1= citas, 2= Vacunas
    notificacion_type = models.IntegerField()
    vacuna = models.ForeignKey(dosisVacunas, on_delete=models.CASCADE,null=True, blank= True)
    cita = models.ForeignKey(Citas, on_delete=models.CASCADE,null=True, blank= True)
    fecha = models.DateField()
    user_has_seen = models.BooleanField(default=False)
    def __str__(self):
        return str(self.notificacion_type)

    
