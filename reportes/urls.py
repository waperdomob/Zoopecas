
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.decorators import login_required

from reportes import views

urlpatterns = [
    
    path('reportes/', login_required(views.ReportVentasView.as_view()), name='reporte_ventas'),
    

]