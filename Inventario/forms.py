from django import forms

from .models import *

class CategoriasForm(forms.ModelForm):
    class Meta:
        model= Categorias
        fields = ('categoria',)
        widgets = {
	        'categoria':forms.TextInput(attrs={'class':'form-control'}),
        }
        
class ProveedoresForm(forms.ModelForm):
    class Meta:
        model= Proveedores
        fields = ('proveedor','telefono','nombreEmpleado')
        labels = {
            'proveedor': 'Proveedor',
            'telefono': 'Telefono',
            'nombreEmpleado': 'Nombre del Empleado',

        }
        widgets = {
	        'proveedor':forms.TextInput(attrs={'class':'form-control'}),
	        'telefono':forms.TextInput(attrs={'class':'form-control'}),
	        'nombreEmpleado':forms.TextInput(attrs={'class':'form-control'}),
        }
        

class ProductosForm(forms.ModelForm):
    class Meta:
        model= Productos
        fields = '__all__'
        labels = {
            'producto': 'Producto',
            'descripcion': 'Descripcion',
            'cantidad_total': 'Cantidad total',
            'precio_compra': 'Precio compra',
            'precio_venta': 'Precio venta',

        }
        widgets = {
	        'producto':forms.TextInput(attrs={'class':'form-control'}),
            'descripcion':forms.TextInput(attrs={'class':'form-control'}),            
            'cantidad_total':forms.NumberInput(attrs={'class':'form-control'}),
            'precio_compra':forms.NumberInput(attrs={'class':'form-control'}),
            'precio_venta':forms.NumberInput(attrs={'class':'form-control'}),
            'imagen':forms.FileInput(attrs={'class':'form-control'}),
            'categoria':forms.Select(attrs={'class':'form-control'}),
            'proveedor':forms.Select(attrs={'class':'form-control'}),
        }
