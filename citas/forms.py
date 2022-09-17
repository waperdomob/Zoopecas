from django import forms
from .models import *


class CitasForm(forms.ModelForm):
    class Meta:
        model= Citas
        fields = '__all__'

        labels = {
            'fecha' : 'Fecha de la cita',
            'hora':'Hora de la cita',
            'mascota':'Mascota',
            'tipo':'Tipo de cita',

        }
        widgets = {
	        'fecha':forms.DateInput(format=('%Y-%m-%d'),attrs={'class':'form-control','type': 'date'}),
            'hora':forms.TimeInput(attrs={'class':'form-control','type': 'time'}),            
            'mascota':forms.Select(attrs={'class':'form-control'}),
            'tipo':forms.Select(attrs={'class':'form-control'}),
        }
