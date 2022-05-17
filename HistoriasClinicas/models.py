from django.db import models
from django.contrib.auth.models import User
from django.forms import model_to_dict

# Create your models here.

pronostico = (
    ('Favorable','Favorable'),
    ('Desfavorable','Desfavorable'),
    ('Reservado','Reservado'),
)
class Cargos(models.Model):
    cargo=models.CharField(max_length=45)
    def __str__(self):
        return self.cargo

class Empleados(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    cargo=models.ForeignKey(Cargos,null=False, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.first_name

class Especies(models.Model):
    especie=models.CharField(max_length=45)
    def __str__(self):
        return self.especie

class Razas(models.Model):
    raza=models.CharField(max_length=45)
    def __str__(self):
        return self.raza

class Sexos(models.Model):
    sexo=models.CharField(max_length=45)
    def __str__(self):
        return self.sexo

class Propietarios(models.Model):
    nombrePr=models.CharField(max_length=45)
    direccion=models.CharField(max_length=45)
    telefonos=models.CharField(max_length=45)
    documentoid=models.CharField(max_length=20)
    correo=models.CharField(max_length=45)
    def __str__(self):
        return self.nombrePr
        
    def toJSON(self):
        item = model_to_dict(self)
        return item

class Mascotas(models.Model):
    nombreMas=models.CharField(max_length=45)
    color=models.CharField(max_length=45)
    especie=models.ForeignKey(Especies,null=False, on_delete=models.CASCADE)
    raza=models.ForeignKey(Razas,null=False, on_delete=models.CASCADE)
    sexo=models.ForeignKey(Sexos,null=False, on_delete=models.CASCADE)
    propietario=models.ForeignKey(Propietarios,null=False, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombreMas
        
class HistoriasClinicas(models.Model):
    mascotas=models.ForeignKey(Mascotas,null=False, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    quejaPrincipal=models.CharField(max_length=100)
    tratamientosPrevios=models.CharField(max_length=100)
    enfermedadesAnteriores=models.CharField(max_length=100)
    cirugiasAnteriores=models.CharField(max_length=100)
    dieta = models.CharField(max_length=45)
    medicinaPreventiva = models.CharField(max_length=45)
    temperatura = models.FloatField(help_text='(°C)')
    pulso = models.FloatField(help_text='(X minuto)')
    respiracion = models.FloatField(help_text='(X minuto)')
    inspeccion = models.CharField(max_length=45)
    TLIC = models.FloatField(help_text='(seg)')
    hidratacion = models.FloatField(help_text='(seg)')
    peso = models.FloatField(help_text='(Kg)')
    ganglios = models.CharField(max_length=45)
    sistDigestivo = models.CharField(max_length=45,help_text='(Gusto)')
    sistRespiratorio = models.CharField(max_length=45,help_text='(Olfato)')
    sistCardiovascular = models.CharField(max_length=45)
    sistUrinario = models.CharField(max_length=45)
    sistGenital = models.CharField(max_length=45)
    sistNervioso = models.CharField(max_length=45,help_text='(Visión - Audición)')
    sistLocomotor = models.CharField(max_length=45)
    pielAnexos = models.CharField(max_length=45)
    hallazgos = models.CharField(max_length=200)
    examenesSolicitados=models.CharField(max_length=100)
    examenesAutorizados=models.CharField(max_length=100)
    impresionDiagnostica=models.CharField(max_length=100)
    pronostico=models.CharField(max_length=45)
    tratamientoIdeal=models.CharField(max_length=200)
    cotizacion1=models.IntegerField()
    tratamientoInstaurado=models.CharField(max_length=200)
    cotizacion2=models.IntegerField()
    observaciones=models.CharField(max_length=200)
    veterinario = models.ManyToManyField(Empleados)

    def __str__(self):
        return self.quejaPrincipal

class Seguimiento(models.Model):
    fecha= fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    observaciones = models.CharField(max_length=100)
    responsable = models.ForeignKey(Empleados,null=False, on_delete=models.CASCADE)
    historiaClinica = models.ForeignKey(HistoriasClinicas,null=False, on_delete=models.CASCADE)




    





