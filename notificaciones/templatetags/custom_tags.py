from django import template
import notificaciones
from notificaciones.models import Notificaciones

register = template.Library()

@register.inclusion_tag('show_notifications.html', takes_context= True)
def show_notifications(context):
    notificaciones = Notificaciones.objects.all().exclude(user_has_seen=True).order_by('-fecha')
    return {'notificaciones': notificaciones}