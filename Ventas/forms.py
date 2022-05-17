from tkinter.tix import Select
from django import forms

from .models import *

class VentasForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'


    class Meta:
        model = Venta
        fields = '__all__'
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control select2','style': 'width: 100%'}),
            'fecha_compra': forms.DateInput(format='%Y-%m-%d',attrs={'class': 'form-control','value': datetime.now().strftime('%Y-%m-%d'),'readonly':True}),
            'metodoPago': forms.Select(attrs={'class': 'form-control select2','style': 'width: 100%'}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control','style': 'width: 100%','readonly': True}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control','style': 'width: 100%'}),
            'total': forms.NumberInput(attrs={'class': 'form-control','style': 'width: 100%','readonly': True}),

        }
