from django import forms
from HistoriasClinicas.models import Mascotas

from .models import *

class dosisVacunasForm(forms.ModelForm):
     class Meta:
        model= dosisVacunas
        exclude = ['mascota']
        labels = {
            'dosis_aplicada': 'Dosis Aplicada',
            'fecha_sgt_dosis': 'Fecha de la siguiente dosis',
            'vacuna': 'Vacuna aplicada',

        }
        widgets = {
	        'dosis_aplicada':forms.NumberInput(attrs={'class':'form-control'}), 
            'fecha_sgt_dosis': forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={'class': 'form-control', 
               'placeholder': 'Select a date',
               'type': 'date'
              }),
            'vacuna':forms.Select(attrs={'class':'form-control'}),

        }