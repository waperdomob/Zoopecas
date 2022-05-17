from django import forms

from HistoriasClinicas.models import Propietarios

class ClientesForm(forms.ModelForm):
    class Meta:
        model= Propietarios
        fields = '__all__'
        labels = {
            'nombrePr': 'Nombre',
            'direccion': 'Dirección',
            'telefonos': 'Telefonos',
            'documentoid': 'Numero de identificación',
            'correo': 'Correo',

        }
        widgets = {
	        'nombrePr':forms.TextInput(attrs={'class':'form-control'}),
            'direccion':forms.TextInput(attrs={'class':'form-control'}),            
            'telefonos':forms.TextInput(attrs={'class':'form-control'}),
            'documentoid':forms.NumberInput(attrs={'class':'form-control'}),
            'correo':forms.TextInput(attrs={'class':'form-control'}),
           
        }