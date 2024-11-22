from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from Clientes import *
from HistoriasClinicas.models import Propietarios
# Register your models here.

class propietariosAdmin(ImportExportModelAdmin):
    list_display=("nombrePr","direccion","telefonos","documentoid","correo",)

admin.site.register(Propietarios,propietariosAdmin)
