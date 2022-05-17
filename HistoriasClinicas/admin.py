from django.contrib import admin
from HistoriasClinicas import *
from HistoriasClinicas.models import Cargos, Empleados, Especies, HistoriasClinicas, Mascotas, Propietarios, Razas, Seguimiento, Sexos
# Register your models here.

class MembershipInline(admin.TabularInline):
    model = HistoriasClinicas.veterinario.through

class empleadosAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline,
    ]

class historiasClinicasAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline,
    ]
    list_display=("id","mascotas","fecha","hora",)


class mascotasAdmin(admin.ModelAdmin):
    list_display=("nombreMas","color","especie")

class propietariosAdmin(admin.ModelAdmin):
    list_display=("nombrePr","direccion","telefonos","documentoid","correo",)



class razasAdmin(admin.ModelAdmin):
    list_display=("raza",)

class especiesAdmin(admin.ModelAdmin):
    list_display=("id","especie",)

class cargosAdmin(admin.ModelAdmin):
    list_display=("cargo",)

class sexosAdmin(admin.ModelAdmin):
    list_display=("sexo",)

class seguimientosAdmin(admin.ModelAdmin):
    list_display=("fecha","hora","observaciones","historiaClinica_id",)


admin.site.register(HistoriasClinicas,historiasClinicasAdmin)
admin.site.register(Mascotas,mascotasAdmin)
admin.site.register(Propietarios,propietariosAdmin)
admin.site.register(Empleados,empleadosAdmin)
admin.site.register(Razas,razasAdmin)
admin.site.register(Especies,especiesAdmin)
admin.site.register(Cargos,cargosAdmin)
admin.site.register(Sexos,sexosAdmin)
admin.site.register(Seguimiento,seguimientosAdmin)
