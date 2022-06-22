from django import template
import datetime as dtime
from datetime import datetime,  timedelta
from django.db.models import Q

import notificaciones
from notificaciones.models import Notificaciones

register = template.Library()

@register.inclusion_tag('show_notifications.html', takes_context= True)
def show_notifications(context):
    d = dtime.date.today() - timedelta(days=3)
    notificaciones = Notificaciones.objects.filter(Q(user_has_seen=False),fecha__range=[d,dtime.date.today()])
    return {'notificaciones': notificaciones}