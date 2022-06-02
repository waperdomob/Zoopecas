from django import forms
from HistoriasClinicas.models import Mascotas

from .models import *

class dosisVacunasForm(forms.ModelForm):
     class Meta:
        model= dosisVacunas
        exclude = ['mascota']
        labels = {
            'dosis_aplicada': 'Dosis Aplicada',
            'vacuna': 'Vacuna aplicada',

        }
        widgets = {
	        'dosis_aplicada':forms.NumberInput(attrs={'class':'form-control'}), 
            'vacuna':forms.Select(attrs={'class':'form-control'}),

        }