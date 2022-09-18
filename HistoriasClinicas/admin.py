from django.contrib import admin
from HistoriasClinicas import *
from HistoriasClinicas.models import Cargos, Empleados, HistoriasClinicas, Seguimiento
# Register your models here.

class MembershipInline(admin.TabularInline):
    model = HistoriasClinicas.veterinario.through

class empleadosAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline,
    ]
    list_display=("id","user")

class historiasClinicasAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline,
    ]
    list_display=("id","mascotas","fecha","hora",)

class cargosAdmin(admin.ModelAdmin):
    list_display=("cargo",)


class seguimientosAdmin(admin.ModelAdmin):
    list_display=("fecha","hora","observaciones","historiaClinica_id",)


admin.site.register(HistoriasClinicas,historiasClinicasAdmin)
admin.site.register(Cargos,cargosAdmin)
admin.site.register(Empleados,empleadosAdmin)
admin.site.register(Seguimiento,seguimientosAdmin)
