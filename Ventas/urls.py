
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.decorators import login_required

from Ventas import views

urlpatterns = [
    
    path('Venta/add/', login_required(views.SaleCreateView.as_view()), name='venta_create'),
    path('sale/list/', login_required(views.SaleListView.as_view()), name='venta_list'),
    path('sale/edit/<int:pk>/',login_required(views.SaleEditView.as_view()), name='venta_editar'),
    path('sale/eliminar/<int:pk>/',login_required(views.SaleDeleteView.as_view()), name='venta_eliminar'),

]