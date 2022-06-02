from unicodedata import name
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.urls import path,include
from django.contrib.auth.decorators import login_required

from HistoriasClinicas import views
from Inventario import views

urlpatterns = [
    path('crear_producto/',login_required(views.crearProductos.as_view()), name='crearProducto'),
    path('inventario/',login_required(views.listaProductos.as_view()), name='inventario'),
    path('inventario/eliminar/<int:pk>/',login_required(views.deleteProducto.as_view()), name='eliminarProducto'),
    path('inventario/edit/<int:pk>/',login_required(views.ProductoUpdate.as_view()), name='editarProducto'),
    path('categorias/',views.create_categoria, name='categoria'),
    path('categorias/eliminar/<int:pk>/',login_required(views.deleteCategoria.as_view()), name='eliminarCategoria'),
    path('categorias/edit/<int:pk>/',login_required(views.CategoriaUpdate.as_view()), name='editarCategoria'),
    path('crear_proveedor/',login_required(views.crearProveedor.as_view()), name='crearProveedor'),
    path('proveedores/',login_required(views.listaProveedores.as_view()), name='proveedores'),
    path('proveedor/eliminar/<int:pk>/',login_required(views.deleteProovedor.as_view()), name='eliminarProveedor'),
    path('proveedor/edit/<int:pk>/',login_required(views.ProovedorUpdate.as_view()), name='editarProveedor'),
    path('vacunas/',login_required(views.listaVacunas.as_view()), name='vacunas'),
    path('registrar_vacuna/',login_required(views.registrarVacunas.as_view()), name='registrarVacuna'),
    path('Vacuna/eliminar/<int:pk>/',login_required(views.deleteVacuna.as_view()), name='eliminarVacuna'),
    path('Vacuna/edit/<int:pk>/',login_required(views.VacunaUpdate.as_view()), name='editarVacuna'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)