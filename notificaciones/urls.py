from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path,include
from django.urls import re_path
from notificaciones import views


urlpatterns = [
       
    path('notificaciones/<int:notificacion_pk>',login_required(views.PostNoficacion.as_view()), name='notificaciones'),
    path('notificaciones/delete/<int:notificacion_pk>',login_required(views.RemoveNoficacion.as_view()), name='notification-delete'),

]