from django.db import models
from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.conf import settings

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
    nombrePr=models.CharField(max_length=100)
    direccion=models.CharField(max_length=100)
    telefonos=models.CharField(max_length=100)
    documentoid=models.CharField(max_length=20)
    correo=models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.nombrePr
        
    def toJSON(self):
        item = model_to_dict(self)
        return item

class Mascotas(models.Model):
    foto = models.ImageField(upload_to='mascotas/', null= True, blank = True)
    nombreMas=models.CharField(max_length=45)
    color=models.CharField(max_length=45)
    edad = models.DateField(null=True)
    especie=models.ForeignKey(Especies,null=False, on_delete=models.CASCADE)
    raza=models.ForeignKey(Razas,null=False, on_delete=models.CASCADE)
    sexo=models.ForeignKey(Sexos,null=False, on_delete=models.CASCADE)
    caracteristicas = models.CharField(max_length=100,null=True)
    propietario=models.ForeignKey(Propietarios,null=False, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombreMas+"→"+self.propietario.nombrePr

    def toJSON(self):
        item = model_to_dict(self)
        item['especie'] = self.especie.toJSON()
        item['raza'] = self.raza.toJSON()
        item['foto'] = self.get_image()        
        item['sexo'] = self.sexo.toJSON()
        item['propietario'] = self.propietario.toJSON()
        return item
    
    def get_image(self):
        if self.foto:
            return '{}{}'.format(settings.MEDIA_URL, self.foto)
        return '{}{}'.format(settings.STATIC_URL, 'img/veterinariaHC.jpg')  

class HistoriasClinicas(models.Model):
    mascotas=models.ForeignKey(Mascotas,null=False, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    quejaPrincipal=models.CharField(max_length=250)
    tratamientosPrevios=models.CharField(max_length=250)
    enfermedadesAnteriores=models.CharField(max_length=250)
    cirugiasAnteriores=models.CharField(max_length=250)
    dieta = models.CharField(max_length=250)
    medicinaPreventiva = models.CharField(max_length=250)
    temperatura = models.FloatField(help_text='(°C)')
    pulso = models.FloatField(help_text='(X minuto)')
    respiracion = models.FloatField(help_text='(X minuto)')
    inspeccion = models.CharField(max_length=250)
    TLIC = models.FloatField(help_text='(seg)')
    hidratacion = models.FloatField(help_text='(%)')
    peso = models.FloatField(help_text='(Kg)')
    ganglios = models.CharField(max_length=250)
    sistDigestivo = models.CharField(max_length=250,help_text='(Gusto)')
    sistRespiratorio = models.CharField(max_length=250,help_text='(Olfato)')
    sistCardiovascular = models.CharField(max_length=250)
    sistUrinario = models.CharField(max_length=250)
    sistGenital = models.CharField(max_length=250)
    sistNervioso = models.CharField(max_length=250,help_text='(Visión - Audición)')
    sistLocomotor = models.CharField(max_length=250)
    pielAnexos = models.CharField(max_length=250)
    hallazgos = models.CharField(max_length=250)
    examenesSolicitados=models.CharField(max_length=100)
    examenesAutorizados=models.CharField(max_length=250)
    impresionDiagnostica=models.CharField(max_length=250)
    pronostico=models.CharField(max_length=250)
    tratamientoIdeal=models.CharField(max_length=250)
    cotizacion1=models.IntegerField()
    tratamientoInstaurado=models.CharField(max_length=250)
    cotizacion2=models.IntegerField()
    observaciones=models.CharField(max_length=250)
    consideraciones = models.TextField(null= True, blank=True)
    veterinario = models.ManyToManyField(Empleados)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.quejaPrincipal

class Documento(models.Model):
    historia_clinica = models.ForeignKey(HistoriasClinicas, related_name='documentos', on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='documentos/')
    titulo = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Documento {self.id} - {self.historia_clinica}"

class Seguimiento(models.Model):
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    observaciones = models.CharField(max_length=250)
    responsable = models.ForeignKey(Empleados,null=False, on_delete=models.CASCADE)
    historiaClinica = models.ForeignKey(HistoriasClinicas,null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.observaciones

class documentosAd(models.Model):
    """
    Documentos adicionales de la historia clinica.
    """
    titulo = models.CharField(max_length=100)
    documentoAD  = models.FileField(null=True, blank=True)
    historiaClinica = models.ForeignKey(HistoriasClinicas, on_delete=models.CASCADE)
    def __str__(self):
        return self.titulo





