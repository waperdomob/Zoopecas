from logging import PlaceHolder
from django import forms

from .models import *



DIETA_CHOICES = (
    ('Concentrado','Concentrado'),
    ('Barf','Barf'),
    ('Cacera','Cacera'),
    ('Mixta','Mixta'),
    ('Otra','Otra'),

)
PRONOSTICOS = (
    ('Favorable','Favorable'),
    ('Desfavorable','Desfavorable'),
    ('Reservado','Reservado'),

)
class SearchForm(forms.Form):
    documento = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Número del documento'}))

class PropietariosForm(forms.ModelForm):
    class Meta:
        model= Propietarios
        fields = '__all__'

        labels = {
            'documentoid' : 'Número de identificación',
            'nombrePr':'Nombre',
            'telefonos':'Telefono',

        }
        widgets = {
	        'nombrePr':forms.TextInput(attrs={'class':'form-control'}),
            'direccion':forms.TextInput(attrs={'class':'form-control'}),            
            'telefonos':forms.TextInput(attrs={'class':'form-control','placeholder':'3001010123'}),
            'documentoid':forms.TextInput(attrs={'class':'form-control'}),
            'correo':forms.TextInput(attrs={'class':'form-control'}),
        }

class MascotasForm(forms.ModelForm):
    class Meta:
        model= Mascotas
        fields = '__all__'

        labels = {
            'nombreMas':'nombre',
        }
        widgets = {
	        'nombreMas':forms.TextInput(attrs={'class':'form-control'}),
	        'foto':forms.FileInput(attrs={'class':'form-control'}),
            'edad':forms.DateInput(format=('%Y-%m-%d'),attrs={'class':'form-control','type': 'date'}),
            'color':forms.TextInput(attrs={'class':'form-control'}),           
            'especie':forms.Select(attrs={'class':'form-control'}),
            'raza':forms.Select(attrs={'class':'form-control'}),
            'sexo':forms.Select(attrs={'class':'form-control'}),
            'caracteristicas':forms.TextInput(attrs={'class':'form-control'}),
            'propietario':forms.Select(attrs={'class':'form-control'}),
        }
        def clean_rowname(self):
            return self.cleaned_data['foto'] or None
class HistoriasCForm(forms.ModelForm):

    class Meta:
        model= HistoriasClinicas
        #exclude = ['mascotas']
        fields = '__all__'
        labels = {
            'quejaPrincipal':'Queja principal',
            'tratamientosPrevios':'Tratamientos Previos',
            'enfermedadesAnteriores':'Enfermedades Anteriores',
            'cirugiasAnteriores':'Cirugias Anteriores',
            'dieta':'Dieta',
            'medicinaPreventiva':'Medicina Preventiva',
            'inspeccion':'Inspección',
            'TLIC':'T. LI. C.',
            'sistDigestivo':'A. Sistema Digestivo',
            'sistRespiratorio':'B. Sistema Respiratorio',
            'sistCardiovascular':'C. Sistema Cardiovascular',
            'sistUrinario':'D. Sistema Urinario',
            'sistGenital':'E. Sistema Genital',
            'sistNervioso':'F. Sistema Nervioso',
            'sistLocomotor':'G. Sistema Locomotor',
            'pielAnexos':'Piel y Anexos',
            'hallazgos':'Hallazgos',
            'examenesSolicitados':'Examenes Solicitados',
            'examenesAutorizados':' Examenes Autorizados',
            'impresionDiagnostica':'Impresion Diagnostica',
            'pronostico':'Pronostico',
            'tratamientoIdeal':'Tratamiento Ideal',
            'cotizacion1':'Cotizacion 1',
            'tratamientoInstaurado':'Tratamiento Instaurado',
            'cotizacion2':'Cotizacion 2',
            'veterinario':'MEDICO VETERINARIO',


        }
        widgets = {
            'mascotas':forms.Select(attrs={'class':'form-control'}),
	        'quejaPrincipal':forms.TextInput(attrs={'class':'form-control'}),
            'tratamientosPrevios':forms.TextInput(attrs={'class':'form-control'}),            
            'enfermedadesAnteriores':forms.TextInput(attrs={'class':'form-control'}),
            'cirugiasAnteriores':forms.TextInput(attrs={'class':'form-control'}), 
            'dieta':forms.CheckboxSelectMultiple(attrs={'class':'cajaCheck radio-checkbox'},choices=DIETA_CHOICES),
            'medicinaPreventiva':forms.TextInput(attrs={'class':'form-control'}), 
            'inspeccion':forms.TextInput(attrs={'class':'form-control'}),
            'temperatura':forms.NumberInput(attrs={'class':'form-control '}),
            'pulso':forms.NumberInput(attrs={'class':'form-control'}), 
            'respiracion':forms.NumberInput(attrs={'class':'form-control'}),
            'TLIC':forms.NumberInput(attrs={'class':'form-control'}), 
            'hidratacion':forms.NumberInput(attrs={'class':'form-control'}),
            'peso':forms.NumberInput(attrs={'class':'form-control'}),
            'ganglios':forms.TextInput(attrs={'class':'form-control'}),
            'sistDigestivo':forms.TextInput(attrs={'class':'form-control'}),            
            'sistRespiratorio':forms.TextInput(attrs={'class':'form-control'}),
            'sistCardiovascular':forms.TextInput(attrs={'class':'form-control'}), 
            'sistUrinario':forms.TextInput(attrs={'class':'form-control'}),
            'sistGenital':forms.TextInput(attrs={'class':'form-control'}), 
            'sistNervioso':forms.TextInput(attrs={'class':'form-control'}),
            'sistLocomotor':forms.TextInput(attrs={'class':'form-control'}),            
            'pielAnexos':forms.TextInput(attrs={'class':'form-control'}),
            'hallazgos':forms.TextInput(attrs={'class':'form-control'}), 
            'examenesSolicitados':forms.TextInput(attrs={'class':'form-control'}),
            'examenesAutorizados':forms.TextInput(attrs={'class':'form-control'}), 
            'impresionDiagnostica':forms.TextInput(attrs={'class':'form-control'}),
            'pronostico':forms.CheckboxSelectMultiple(attrs={'class':'cajaCheck radio-checkbox'},choices=PRONOSTICOS), 
            'tratamientoIdeal':forms.TextInput(attrs={'class':'form-control'}),
            'cotizacion1':forms.NumberInput(attrs={'class':'form-control'}), 
            'tratamientoInstaurado':forms.TextInput(attrs={'class':'form-control'}),
            'cotizacion2':forms.NumberInput(attrs={'class':'form-control'}),
            'observaciones':forms.Textarea(attrs={'class':'form-control','rows': 3}),
            'veterinario':forms.SelectMultiple(attrs={'class':'form-control '}),

        }

class SeguimientoForm(forms.ModelForm):

    class Meta:
        model= Seguimiento
        exclude = ('historiaClinica',)

        widgets = {
            'observaciones':forms.Textarea(attrs={'class':'form-control','rows': 3}),
	        'responsable':forms.Select(attrs={'class':'form-control'}),
            'historiaClinica':forms.Select(attrs={'class':'form-control'}),
        }

class docsADForm(forms.ModelForm):
    class Meta:
        model= documentosAd
        exclude = ['titulo','historiaClinica']
        labels = {
            'documentoAD' : 'Documentos adicionales',
        }
        widgets = {          
            'documentoAD':forms.FileInput(attrs={'class': 'form-control','multiple':True}),
            
        }