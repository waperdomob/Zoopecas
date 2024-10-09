from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from HistoriasClinicas import *
from HistoriasClinicas.models import Cargos, Empleados, HistoriasClinicas, Seguimiento
from HistoriasClinicas.resources import HistoriasClinicasResource
# Register your models here.

class MembershipInline(admin.TabularInline):
    model = HistoriasClinicas.veterinario.through

class empleadosAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline,
    ]
    list_display=("id","user")

@admin.register(HistoriasClinicas)
class HistoriasClinicasAdmin(ImportExportModelAdmin):
    resource_class = HistoriasClinicasResource

class cargosAdmin(admin.ModelAdmin):
    list_display=("cargo",)


class seguimientosAdmin(admin.ModelAdmin):
    list_display=("fecha","hora","observaciones","historiaClinica_id",)


admin.site.register(Cargos,cargosAdmin)
admin.site.register(Empleados,empleadosAdmin)
admin.site.register(Seguimiento,seguimientosAdmin)
