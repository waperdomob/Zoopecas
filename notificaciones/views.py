from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from requests import request
from mascotas.models import dosisVacunas

from notificaciones.models import Notificaciones

# Create your views here.

class PostNoficacion(View):

    def get(self, request, notificacion_pk, *args, **kwargs):
        notificacion = Notificaciones.objects.get(pk = notificacion_pk)
        notificacion.user_has_seen = True
        notificacion.save()
        return redirect('inicio')

class RemoveNoficacion(View):

    def delete(self, request, notificacion_pk, *args, **kwargs):
        notificacion = Notificaciones.objects.get(pk = notificacion_pk)
        notificacion.user_has_seen = True
        notificacion.save()
        return HttpResponse('Success', content_type= 'text/plain')
    