from django.contrib import admin
from mascotas.models import *
# Register your models here.
class vacunasAdmin(admin.ModelAdmin):   
    list_display=("id","vacuna","cantidad","dosis",)

class dosisAdmin(admin.ModelAdmin):   
    list_display=("id","dosis_aplicada","fecha_aplicacion","mascota","vacuna")

admin.site.register(Vacunas,vacunasAdmin)
admin.site.register(dosisVacunas,dosisAdmin)