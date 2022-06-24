from django.contrib import admin
from citas.models import Citas,TipoCita
# Register your models here.


class tipoCitasAdmin(admin.ModelAdmin):
    list_display=("tipodeCita",)


class citasAdmin(admin.ModelAdmin):
    list_display=("fecha","hora","mascota","tipo",)

admin.site.register(TipoCita,tipoCitasAdmin)
admin.site.register(Citas,citasAdmin)