from django.contrib import admin
from Clientes import *
from HistoriasClinicas.models import Propietarios
# Register your models here.

class propietariosAdmin(admin.ModelAdmin):
    list_display=("nombrePr","direccion","telefonos","documentoid","correo",)

admin.site.register(Propietarios,propietariosAdmin)
