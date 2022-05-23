from django.forms import *
from Inventario import models
CHOICES=(
    ("0","Elija una opción"),
    ("1", "Efectivo"),
    ("2", "Datafono"),
    ("3", "Daviplata"),
    ("4", "Nequi"),

)
CHOICES2=(
    ("0","Elija una opción"),
    ("1", "Concentrados"),
    ("2", "Accesorios"),
    ("3", "Drogueria"),
    ("4", "Peluqueria"),
    ("5", "Consultorio"),

)
class reportForm(Form):
    
    date_range = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))
    Metodo_pago = ChoiceField(widget=Select(attrs={
        'class': 'form-control'
    }),choices=CHOICES)

    categoria = ChoiceField(widget=Select(attrs={
        'class':'form-control'
    }),choices=CHOICES2)