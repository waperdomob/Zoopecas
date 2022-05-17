from django.forms import *

CHOICES=(
    ("0","Elija una opción"),
    ("1", "Efectivo"),
    ("2", "Datafono"),
    ("3", "Daviplata"),
    ("4", "Nequi"),

)
class reportForm(Form):
    
    date_range = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))
    Metodo_pago = ChoiceField(widget=Select(attrs={
        'class': 'form-control'
    }),choices=CHOICES)
