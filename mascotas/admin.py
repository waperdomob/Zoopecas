from django.contrib import admin
from mascotas.models import *
from HistoriasClinicas.models import  Especies, Mascotas, Razas , Sexos

# Register your models here.
class mascotasAdmin(admin.ModelAdmin):
    list_display=("id","foto","nombreMas","color","especie")

class razasAdmin(admin.ModelAdmin):
    list_display=("raza",)

class especiesAdmin(admin.ModelAdmin):
    list_display=("id","especie",)

class sexosAdmin(admin.ModelAdmin):
    list_display=("sexo",)

class vacunasAdmin(admin.ModelAdmin):   
    list_display=("id","vacuna","cantidad","dosis",)

class dosisAdmin(admin.ModelAdmin):   
    list_display=("id","dosis_aplicada","fecha_aplicacion","mascota","vacuna")

admin.site.register(Mascotas,mascotasAdmin)
admin.site.register(Razas,razasAdmin)
admin.site.register(Especies,especiesAdmin)
admin.site.register(Sexos,sexosAdmin)
admin.site.register(Vacunas,vacunasAdmin)
admin.site.register(dosisVacunas,dosisAdmin)